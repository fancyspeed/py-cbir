#!/usr/bin/env python
# coding: utf-8
import os.path

demo_port = 19999

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
}
