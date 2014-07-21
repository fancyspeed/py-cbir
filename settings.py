#!/usr/bin/env python
# coding: utf-8

import os.path

settings = {
	"sitename": "CBIR demo",
	"template_path": os.path.join(os.path.dirname(__file__), "templates"),
	"static_path": os.path.join(os.path.dirname(__file__), "static"),
	"xsrf_cookies": False,
	"cookie_secret": "23i8ik2KOW9kajf9EW8aJmv0/R4=",
	"login_url": "/auth/login",
	"autoescape": None,
	"debug": True,
}

db = {
	#"host": sae.const.MYSQL_HOST,
	#"port": sae.const.MYSQL_PORT,
	#"db": sae.const.MYSQL_DB,
	#"user": sae.const.MYSQL_USER,
	#"password": sae.const.MYSQL_PASS,
}
