#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from flask import Flask, render_template, request
import flask, random

import pprint

# configuration
class Config(object):
	DEBUG = False
	TESTING = False
	SECRET_KEY = str(random.randint(1,1000))
	USERNAME = 'admin'
	PASSWORD = 'admin'

class ProductionConfig(Config):
	pass 

class DevelopmentConfig(Config):
	DEBUG = True

class TestingConfig(Config):
	TESTING = True

class RhythmRemoteWebServer(object):
	def __init__(self):
		self.app = flask.Flask(__name__)
		self.app.config.from_object(ProductionConfig)
		self.routes = Routes(self)
		self.loadRoutes()
		self.app.before_request(self.force_login)
		self.app.run(use_reloader=False)
	
	def loadRoutes(self):
		self.app.add_url_rule('/', 'index', self.routes.index)
		self.app.add_url_rule(
			'/login', 
			'login', 
			self.routes.login, 
			**{'methods': ['GET', 'POST']}
		)
		self.app.add_url_rule(
			'/logout', 
			'logout', 
			self.routes.logout
		)
	
	def force_login(self):
		if flask.request.path != '/login' and \
			flask.request.path[:7] != '/static':
			try:
				if flask.session['logged_in']:
					pass
			except KeyError:
				return flask.redirect(flask.url_for('login'))		
		
class Routes(object):
	def __init__(self, server):
		self.server = server
		
	def index(self):
		return flask.render_template('index.html')

	def login(self):
		error = None
		if flask.request.method == 'POST':
			if flask.request.form['username'] != self.server.app.config['USERNAME']:
				error = 'Invalid username'
			elif flask.request.form['password'] != self.server.app.config['PASSWORD']:
				error = 'Invalid password'
			else:
				flask.session['logged_in'] = True
				flask.flash('You were logged in')
				return flask.redirect(flask.url_for('index'))
		return flask.render_template('login.html', error=error)
	
	def logout(self):
		flask.session.pop('logged_in', None)
		flask.flash('You were logged out')
		return flask.redirect(flask.url_for('index'))


if __name__ == '__main__':
	server = RhythmRemoteWebServer() 
