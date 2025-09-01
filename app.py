from flask import Flask, jsonify, request
import sqlite3

conn = sqlite3.connect('larm.db')
cursor = conn.cursor()

