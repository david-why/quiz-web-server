from flask import render_template


def alert(msg, redirect=None):
    return render_template('alert.html', msg=msg, redirect=redirect)
