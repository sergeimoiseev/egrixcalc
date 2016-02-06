# -*- coding: utf-8 -*-
import flask, flask.views
import calc_tools as ct
import params_processor as proc
import logging

logger = logging.getLogger(__name__)

app = flask.Flask(__name__)
app.debug = True
app.secret_key = "bacon"

default_params, params_comments = ct.get_and_store_params(load_from_dropbox=False)

class Main(proc.EgrixCalcView):
    def get(self):
        return flask.render_template('index.html')

    def post(self):
        logger.info("post request in Main")

        messages_to_flash = self.process_params('index')
        
        flask.flash(messages_to_flash[0])
        flask.flash(messages_to_flash[1])

        return flask.redirect(flask.url_for('index'))

class TypeArbitary(proc.EgrixCalcView):
    def get(self):
        return flask.render_template('type_arbitary.html')

    def post(self):
        logger.info("post request in TypeArbitary")

        messages_to_flash = self.process_params('type_arbitary')

        flask.flash(messages_to_flash[0])
        flask.flash(messages_to_flash[1])

        return flask.redirect(flask.url_for('type_arbitary'))

app.add_url_rule('/',
        view_func=Main.as_view('index'),
        methods=['GET', 'POST'])

app.add_url_rule('/type_arbitary/', 
        view_func=TypeArbitary.as_view('type_arbitary'),
        methods=['GET', 'POST'])

if __name__ == '__main__':
    ct.setup_logging()
    app.run()