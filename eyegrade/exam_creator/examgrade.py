import sys
import webbrowser

# Local imports
import eyegrade.utils as utils
import exam_gui as gui
import eyegrade.exammaker as exammaker


class ProgramManager(object):
    def __init__(self, interface):
        self.interface = interface
        self.listQuestions = []
        # Listeners
        self._register_listeners()

    def run(self):
        """Starts the program manager."""
        self.interface.run()

    def _register_listeners(self):
        listeners = {
            ('actions', 'help', 'help'): self._action_help,
            ('actions', 'help', 'website'): self._action_website,
            ('actions', 'help', 'source'): self._action_source_code,
            # Create exam button
            ('center', 'exam', 'info', 'button'): self._create_exam,
        }
        self.interface.register_listeners(listeners)

    def _action_help(self):
        """Callback for the help action."""
        webbrowser.open(utils.help_location, new=2)

    def _action_website(self):
        """Callback for the website action."""
        webbrowser.open(utils.web_location, new=2)

    def _action_source_code(self):
        """Callback for the source code action."""
        webbrowser.open('https://github.com/jvrplmlmn/eyegrade', new=2)

    def addQuestion(self, question):
        import inspect
        print '%s.%s.%s' % (self.__class__.__module__, self.__class__.__name__, inspect.stack()[0][3])

    def _create_exam(self, subject, degree, title, date, duration):
        print "_create_exam"
        print "\tSubject: \"%s\"" % subject
        print "\tDegree: \"%s\"" % degree
        print "\tTitle: \"%s\"" % title
        print "\tDate: \"%s\"" % date
        print "\tDuration: \"%s\"" % duration

        exam = utils.ExamQuestions()
        exam.subject = subject
        exam.degree = degree
        exam.title = title
        exam.date = date
        exam.duration = duration

        # def __init__(self, num_questions, num_choices, template_filename,
        #              output_file, variables, exam_config_filename,
        #              num_tables=0, dimensions=None,
        #              table_width=None, table_height=None, table_scale=1.0,
        #              id_box_width=None,
        #              force_config_overwrite=False, score_weights=None,
        #              left_to_right_numbering=False, survey_mode=False):
        # At least 1 option and 2 choices are necessary to create an exam:
        import os
        num_questions = 1
        num_choices = 2
        #template_filename = 'template_filename'
        # ../../doc/sample-files/template.tex
        template_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                         '../../doc/sample-files/template.tex')
        output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   'output_file-%s.tex')
        #output_file = sys.stdout
        variables = {'subject': subject,
                     'degree': degree,
                     'title': title,
                     'date': date,
                     'duration': duration }

        # If exam_config_filename is None > _new_exam_config()
        #       => exam.config = eyegrade.utils.ExamConfig()
        # If exam_config_filename is Not None > _load_exam_config()
        exam_config_filename = None
        # exam_config_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
        #                                     '../../doc/sample-files/exam.eye')

        maker = exammaker.ExamMaker(num_questions, num_choices,
                                    template_filename,
                                    output_file, variables, exam_config_filename,
                                    force_config_overwrite=True)
        print '\tmaker.num_questions', maker.num_questions
        print '\tmaker.num_choices', maker.num_choices
        print '\tmaker.parts', maker.parts
        print '\tmaker.left_to_right_numbering', maker.left_to_right_numbering
        print '\tmaker.survey_mode', maker.survey_mode
        print '\tmaker.output_file', maker.output_file
        print '\tmaker.exam_questions', maker.exam_questions
        print '\tmaker.exam_config_filename', maker.exam_config_filename
        print '\tmaker.dimensions', maker.dimensions
        print '\tmaker.table_scale', maker.table_scale
        print '\tmaker.id_box_width', maker.id_box_width
        print '\tmaker.table_width', maker.table_width
        print '\tmaker.table_height', maker.table_height
        print '\tmaker.exam_config', maker.exam_config
        print '\tmaker.empty_variables', maker.empty_variables

        # def create_exam(self, model, shuffle, with_solution=False):
        #     """Creates a new exam.
        #
        #        'shuffle' must be a boolean. If True, the exam is shuffled
        #        again even if it was previously shuffled. If False, it is
        #        only shuffled if it was not previously shuffled.
        #
        #     """
        models = '0A'
        dont_shuffle_again = False
        for model in models:
            print '\tCreating exam for model:', model
            maker.create_exam(model, not dont_shuffle_again)

def main():
    if len(sys.argv) >= 2:
        file = sys.argv[1]
    else:
        file = None
    interface = gui.Interface(file, [])
    manager = ProgramManager(interface)
    manager.run()

if __name__ == '__main__':
    main()