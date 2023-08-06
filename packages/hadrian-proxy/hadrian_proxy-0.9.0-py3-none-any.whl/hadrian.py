"""Hadrian authenticated proxy."""
__version__ = "0.9.0"

import asyncio
import mimetypes
import pathlib
import secrets
import sys


import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
import tornado.httputil


tornado.options.define("cookie_secret", default=None, help="Cookie signing secret")
tornado.options.define("cookie_life", default=1, help="Cookie life in days")
tornado.options.define("port", default=8080, help="Port")
tornado.options.define("password", help="Password")
tornado.options.define("backend", help="Backend: proxy or filesystem")
tornado.options.define("root", help="Root: proxy address or filesystem path")
tornado.options.define("login_page", default="_login", help="Url path for login endpoint")

PROXY_BLACKLIST_HEADERS = ("Content-Length", "Transfer-Encoding", "Content-Encoding", "Connection")


def get_contenttype(fp):
	mime_type, encoding = mimetypes.guess_type(fp.as_posix())
	if encoding == "gzip":
			return "application/gzip"
	elif encoding is not None:
			return "application/octet-stream"
	elif mime_type is not None:
			return mime_type
	else:
			return "application/octet-stream"


class FilesystemBackend():
	def __init__(self, root):
		self.root = pathlib.Path(root).resolve()
		if not self.root.is_dir():
			raise RuntimeError("Root does not exist", self.root)

	async def handle(self, req, handler):
		fp = (self.root / req.path.lstrip("/")).resolve()
		if fp.is_dir():
			fp = fp / "index.html"
		try:
			fp.relative_to(self.root)
		except ValueError:
			handler.set_status(500)
			handler.write("Invalid access")
			handler.write(req.path)
		else:
			if fp.is_file():
				handler.add_header("Content-Type", get_contenttype(fp))
				with fp.open("rb") as fh:
					handler.set_status(200)
					handler.write(fh.read())
			else:
				handler.set_status(404)
				handler.write("Missing: ")
				handler.write(req.path)
		handler.finish()


class ProxyBackend():
	def __init__(self, root):
		self.root = root

	async def handle(self, req, handler):
		body = req.body or None
		req = tornado.httpclient.HTTPRequest(
			self.root + req.uri,
			method = req.method,
			body = req.body or None,
			headers = req.headers,
			follow_redirects = False,
		)
		client = tornado.httpclient.AsyncHTTPClient()
		try:
			resp = await client.fetch(req, raise_error=False)
		except ConnectionError as e:
			handler.set_status(500)
			handler.write("Error from upstream:\n")
			handler.write(e.strerror)
		else:
			handler.set_status(resp.code, resp.reason)
			handler._headers = tornado.httputil.HTTPHeaders()
			for header, v in resp.headers.get_all():
				if header not in PROXY_BLACKLIST_HEADERS:
					handler.add_header(header, v)
			if resp.body:
				handler.set_header("Content-Length", len(resp.body))
				handler.write(resp.body)
		handler.finish()


class ProtectedHandler(tornado.web.RequestHandler):
	def compute_etag(self):
		return None

	def initialize(self, backend, options):
		self.backend = backend
		self.options = options

	def get_current_user(self):
		c = self.get_secure_cookie("hadrian_user", max_age_days=self.options.cookie_life)
		if c is None:
			return None
		c = c.decode("utf-8")
		x_real_ip = self.request.headers.get("X-Real-IP", "na")
		if c != x_real_ip:
			return None
		return c

	async def get(self, url):
		if self.get_current_user():
			await self.backend.handle(self.request, self)
		else:
			self.redirect(self.options.login_page)

	async def post(self, url):
		if self.get_current_user():
			await self.backend.handle(self.request, self)
		else:
			self.set_status(403, "No auth")
			self.finish()


class LoginHandler(tornado.web.RequestHandler):
	def compute_etag(self):
		return None

	def initialize(self, options):
		self.options = options

	def get(self):
		self.write("""
		<html>
		<body>
		<form action="" method="POST">
			<input type="password" name="password" />
			<input type="submit" value="Sign in" />
		</form>
		</body>
		""")

	def post(self):
		inp = self.get_argument("password")
		if inp == self.options.password:
			x_real_ip = self.request.headers.get("X-Real-IP", "na")
			self.set_secure_cookie(
				"hadrian_user",
				x_real_ip,
				expires_days=self.options.cookie_life,
			)
			self.redirect("/")
		else:
			self.redirect(self.options.login_page)


def run(options):
	if options.cookie_secret is None:
		options.cookie_secret = secrets.token_hex(32)
	if options.backend == "proxy":
		backend = ProxyBackend(options.root)
	elif options.backend == "filesystem":
		backend = FilesystemBackend(options.root)
	else:
		raise RuntimeError("No such backend")
	routes = [
		("/" + options.login_page, LoginHandler, {"options": options}),
		(r"/(.*)", ProtectedHandler, {"backend": backend, "options": options}),
	]
	app = tornado.web.Application(
		routes,
		cookie_secret = options.cookie_secret,
		debug = True,
	)
	app.listen(options.port)
	ioloop = tornado.ioloop.IOLoop.instance()
	ioloop.start()


if __name__ == "__main__":
	try:
		fn = sys.argv[1]
	except IndexError:
		print("Usage: python -m hadrian config.conf")
	else:
		tornado.options.parse_config_file(fn)
		run(tornado.options.options)
