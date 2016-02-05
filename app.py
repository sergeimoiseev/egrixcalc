# -*- coding: utf-8 -*-
import flask, flask.views
# import egrix_calc
# import calc_tools as ct
# import params_processor as proc
import logging
logger = logging.getLogger(__name__)

app = flask.Flask(__name__)
app.debug = True
app.secret_key = "bacon"

class Main(proc.EgrixCalcView):
    def get(self):
        return flask.render_template('index.html')
        
    def post(self):
        logger.info("post request in Main")

        # messages_to_flash = self.process_params('index')
        # logger.info("messages_to_flash\n%s" % (messages_to_flash,))
        # for message in messages_to_flash:
        #     flask.flash(message)

        return flask.redirect(flask.url_for('index'))

class TypeArbitary(proc.EgrixCalcView):
    def get(self):
        return flask.render_template('type_arbitary.html')
        
    def post(self):
        logger.info("post request in TypeArbitary")

        # messages_to_flash = self.process_params('type_arbitary')
        # logger.info("messages_to_flash\n%s" % (messages_to_flash,))
        # for message in messages_to_flash:
        #     flask.flash(message)
            
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