
from bqplot import *
from bqplot.marks import Graph
from copy import deepcopy

from IPython.display import display

from .input import valid_path, valid_string
from .constants import INPUT_NAME, INPUT_OUTPUT, INPUT_RECIPES, \
    INPUT_TRIGGER_PATH, INPUT_VARIABLES, INPUT_TRIGGER_FILE, \
    INPUT_TRIGGER_OUTPUT, INPUT_NOTEBOOK_OUTPUT, GREEN, RED, \
    INPUT_SOURCE, NOTEBOOK_EXTENSIONS, NAME, DEFAULT_JOB_NAME, \
    SOURCE, PATTERN_NAME, RECIPE_NAME, OBJECT_TYPE, \
    VGRID_PATTERN_OBJECT_TYPE, VGRID_RECIPE_OBJECT_TYPE, \
    VGRID_WORKFLOWS_OBJECT, INPUT_FILE, TRIGGER_PATHS, OUTPUT, RECIPES, \
    VARIABLES, CHAR_UPPERCASE, CHAR_LOWERCASE, CHAR_NUMERIC, CHAR_LINES, \
    VGRID_ERROR_TYPE, VGRID_TEXT_TYPE, PERSISTENCE_ID, VGRID_CREATE, \
    VGRID_UPDATE, PATTERNS, RECIPE, VGRID_DELETE, WIDGET_MODES, VGRID_MODE
from .mig import vgrid_json_call
from .pattern import Pattern, is_valid_pattern_object
from .recipe import is_valid_recipe_dict, create_recipe_dict
from .workflows import build_workflow_object, pattern_has_recipes


def create_widget(patterns=None, recipes=None, mode=VGRID_MODE):
    # TODO update this
    """Displays a widget for workflow definitions. Can optionally take a
    predefined workflow as input"""

    widget = __WorkflowWidget(patterns=patterns,
                              recipes=recipes,
                              mode=mode)
    return widget.display_widget()


class __WorkflowWidget:
    def __init__(self, patterns={}, recipes={}, mode=VGRID_MODE):
        # TODO update this description

        if mode not in WIDGET_MODES:
            raise Exception('Invalide mode requested. Valid modes are: %s'
                            % WIDGET_MODES)
        if not isinstance(patterns, dict):
            raise Exception('The provided patterns were not in a dict')
        for pattern in patterns.values():
            valid, feedback = is_valid_pattern_object(pattern)
            if not valid:
                raise Exception('Pattern %s was not valid. %s'
                                % (pattern, feedback))
        self.patterns = patterns

        if not isinstance(recipes, dict):
            raise Exception('The provided recipes were not in a dict')
        for recipe in recipes.values():
            valid, feedback = is_valid_recipe_dict(recipe)
            if not valid:
                raise Exception('Recipe %s was not valid. %s'
                                % (recipe, feedback))
        self.recipes = recipes

        if patterns and recipes:
            self.workflow = build_workflow_object(patterns, recipes)
        else:
            self.workflow = {}

        self.visualisation_area = widgets.Output()
        self.__update_workflow_visualisation()
        self.display_area = widgets.Output()

        self.new_pattern_button = widgets.Button(
            value=False,
            description="New Pattern",
            disabled=True,
            button_style='',
            tooltip='Define a new pattern'
        )
        self.new_pattern_button.on_click(self.__on_new_pattern_clicked)

        self.edit_pattern_button = widgets.Button(
            value=False,
            description="Edit Pattern",
            disabled=True,
            button_style='',
            tooltip='Edit an existing pattern'
        )
        self.edit_pattern_button.on_click(self.__on_edit_pattern_clicked)

        self.new_recipe_button = widgets.Button(
            value=False,
            description="Add Recipe",
            disabled=True,
            button_style='',
            tooltip='Import a new recipe'
        )
        self.new_recipe_button.on_click(self.__on_new_recipe_clicked)

        self.edit_recipe_button = widgets.Button(
            value=False,
            description="Edit Recipe",
            disabled=True,
            button_style='',
            tooltip='Edit an existing recipe'
        )
        self.edit_recipe_button.on_click(self.__on_edit_recipe_clicked)

        self.import_from_vgrid_button = widgets.Button(
            value=False,
            description="Read VGrid",
            disabled=True,
            button_style='',
            tooltip='Here is a tooltip for this button'
        )
        self.import_from_vgrid_button.on_click(
            self.__on_import_from_vgrid_clicked
        )

        self.export_to_vgrid_button = widgets.Button(
            value=False,
            description="Export Workflow",
            disabled=True,
            button_style='',
            tooltip='Here is a tooltip for this button'
        )
        self.export_to_vgrid_button.on_click(self.__on_export_to_vgrid_clicked)

        self.feedback = widgets.HTML()

        self.current_form = {}
        self.current_old_values = {}
        self.current_form_rows = {}
        self.current_form_line_counts = {}

        self.mig_imports = {
            PATTERNS: {},
            RECIPES: {}
        }

        self.displayed_form = None
        self.editing_area = None
        self.editing = None

        if mode == VGRID_MODE:
            self.__import_from_vgrid(confirm=False)
        self.__enable_top_buttons()

    def __disable_top_buttons(self):
        # TODO update this description

        self.new_pattern_button.disabled = True
        self.edit_pattern_button.disabled = True
        self.new_recipe_button.disabled = True
        self.edit_recipe_button.disabled = True
        self.import_from_vgrid_button.disabled = True
        self.export_to_vgrid_button.disabled = True

    def __enable_top_buttons(self):
        # TODO update this description

        self.new_pattern_button.disabled = False
        if self.patterns:
            self.edit_pattern_button.disabled = False
        else:
            self.edit_pattern_button.disabled = True
        self.new_recipe_button.disabled = False
        if self.recipes:
            self.edit_recipe_button.disabled = False
        else:
            self.edit_recipe_button.disabled = True
        self.import_from_vgrid_button.disabled = False
        self.export_to_vgrid_button.disabled = False

    def __list_current_recipes(self):
        # TODO update this description

        return self.recipes

    def __populate_new_pattern_form(self, population_function, done_function):
        # TODO update this description

        self.current_form[INPUT_NAME] = self.__create_form_single_input(
            "Name",
            "Pattern Name. This is used to identify the pattern and so "
            "should be a unique string."
            "<br/>"
            "Example: <b>pattern_1</b>"
            "<br/>"
            "In this example this pattern is given the name 'pattern_1'.",
            INPUT_NAME
        )
        self.current_form[INPUT_TRIGGER_PATH] = self.__create_form_single_input(
            "Trigger path",
            "Triggering path for file events which are used to schedule "
            "jobs. This is expressed as a regular expression against which "
            "file events are matched. It can be as broad or specific as "
            "required. Any matches between file events and the path given "
            "will cause a scheduled job. File paths are taken relative to the "
            "vgrid home directory. "
            "<br/>"
            "Example: <b>dir/input_file_*\\.txt</b>"
            "<br/>"
            "In this example pattern jobs will trigger on an '.txt' files "
            "whose file name starts with 'input_file_' and is located in "
            "the 'dir' directory. The 'dir' directory in this case should be "
            "located in he vgrid home directory. So if you are operating in "
            "the 'test' vgrid, the structure should be 'test/dir'.",
            INPUT_TRIGGER_PATH
        )
        self.current_form[INPUT_TRIGGER_FILE] = self.__create_form_single_input(
            "Trigger file",
            "This is the variable name used to identify the triggering file "
            "within the job processing."
            "<br/>"
            "Example: <b>input_file</b>"
            "<br/>"
            "In this the triggering file will be copied into the job as "
            "'input_file'. This can then be opened or manipulated as "
            "necessary by the job processing.",
            INPUT_TRIGGER_FILE
        )
        self.current_form[INPUT_TRIGGER_OUTPUT] = self.__create_form_single_input(
            "Trigger output",
            "Trigger output is an optional parameter used to define if the "
            "triggering file is returned. This is defined by the path for the "
            "file to be copied to at job completion. If it is not provided "
            "then any changes made to it are lost, but other output may still "
            "be saved if defined in the output parameter."
            "<br/>"
            "Example: <b>dir/*_output.txt</b>"
            "<br/>"
            "In this example data file is saved within the 'dir' directory. "
            "If the job was triggered on 'test.txt' then the output file "
            "would be called 'test_output.txt",
            INPUT_TRIGGER_OUTPUT,
            optional=True
        )
        self.current_form[INPUT_NOTEBOOK_OUTPUT] = self.__create_form_single_input(
            "Notebook output",
            "Notebook output is an optional parameter used to define if the "
            "notebook used for job processing is returned. This is defined as "
            "a path for the notebook to be copied to at job completion. If it "
            "is not provided then the notebook is destroyed, but other output "
            "may still be saved if defined in the output parameter."
            "<br/>"
            "Example: <b>dir/*_output.ipynb</b>"
            "<br/>"
            "In this example the job notebook is saved within the 'dir' "
            "directory. If the job was triggered on 'test.txt' then the "
            "output notebook would be called 'test_output.ipynb",
            INPUT_NOTEBOOK_OUTPUT,
            optional=True
        )
        self.current_form[INPUT_OUTPUT] = self.__create_form_multi_input(
            "Output",
            "Output data to be saved after job completion. Anything not "
            "saved will be lost. Zero or more files can be copied and should "
            "be expressed in two parts as a variable declaration. The "
            "variable name is the name of the output file within the job, "
            "whilst the value is the file location to which it shall be "
            "copied. In the output string a '*' character can be used to "
            "dynamically create file names, with the * being replaced at "
            "runtime by the triggering files filename. Each output should be "
            "defined in its own text box, and the 'Add output file' button "
            "can be used to create additional text boxes as needed."
            "<br/>"
            "Example: <b>job_output = dir/some_output/*.ipynb</b>"
            "<br/>"
            "In this example, the file 'job_output' is created by the job and "
            "copied to the 'some_output' directory in 'dir'. If 'some_output' "
            "does not already exist it is created. The file will be named "
            "according to the triggering file, and given the '.ipynb' file "
            "extension. If the triggering file was 'sample.txt' then the "
            "output will be called 'sample.ipynb'.",
            INPUT_OUTPUT,
            population_function,
            self.__refresh_new_form,
            done_function=done_function,
            optional=True
        )
        self.current_form[INPUT_RECIPES] = self.__create_form_multi_input(
            "Recipe",
            "Recipe(s) to be used for job definition. These should be recipe "
            "names and may be recipes already defined in the system or "
            "additional ones yet to be added. Each recipe should be defined "
            "in its own text box, and the 'Add recipe' button can be used to "
            "create additional text boxes as needed."
            "<br/>"
            "Example: <b>recipe_1</b>"
            "<br/>"
            "In this example, the recipe 'recipe_1' is used as the definition "
            "of any job processing.",
            INPUT_RECIPES,
            population_function,
            self.__refresh_new_form,
            done_function=done_function,
            extra_text="<br/>Current defined recipes are: ",
            extra_func=self.__list_current_recipes()
        )
        self.current_form[INPUT_VARIABLES] = self.__create_form_multi_input(
            "Variable",
            "Variable(s) accessible to the job at runtime. These are passed "
            "to the job using papermill to run a parameterised notebook. Zero "
            "or more variables can be defined and should be declared as "
            "variable definitions. The variable name will be used as the "
            "variable name within the job notebook, and the vraiable value "
            "will be its value. Any Python data structure can be defined as "
            "long as it can be declared in a single line."
            "<br/>"
            "Example: <b>list_a=[1,2,3]</b>"
            "<br/>"
            "In this example a list of numbers is created and named 'list_a'."
            ,
            INPUT_VARIABLES,
            population_function,
            self.__refresh_new_form,
            done_function=done_function,
            optional=True
        )

    def __populate_editing_pattern_form(
            self, population_function, editing, display_dict):
        # TODO update this description

        self.current_form[INPUT_TRIGGER_PATH] = \
            self.__create_form_single_input(
                "Trigger path",
                "Triggering path for file events which are used to schedule "
                "jobs. This is expressed as a regular expression against "
                "which file events are matched. It can be as broad or "
                "specific as required. Any matches between file events and "
                "the path given will cause a scheduled job. File paths are "
                "taken relative to the vgrid home directory. "
                "<br/>"
                "Example: <b>dir/input_file_*\\.txt</b>"
                "<br/>"
                "In this example pattern jobs will trigger on an '.txt' files "
                "whose file name starts with 'input_file_' and is located in "
                "the 'dir' directory. The 'dir' directory in this case should "
                "be located in he vgrid home directory. So if you are "
                "operating in the 'test' vgrid, the structure should be "
                "'test/dir'.",
                INPUT_TRIGGER_PATH
        )
        self.current_form[INPUT_TRIGGER_FILE] = \
            self.__create_form_single_input(
                "Trigger file",
                "This is the variable name used to identify the triggering "
                "file within the job processing."
                "<br/>"
                "Example: <b>input_file</b>"
                "<br/>"
                "In this the triggering file will be copied into the job as "
                "'input_file'. This can then be opened or manipulated as "
                "necessary by the job processing.",
                INPUT_TRIGGER_FILE
        )
        self.current_form[INPUT_TRIGGER_OUTPUT] = \
            self.__create_form_single_input(
                "Trigger output",
                "Trigger output is an optional parameter used to define if "
                "the triggering file is returned. This is defined by the path "
                "for the file to be copied to at job completion. If it is not "
                "provided then any changes made to it are lost, but other "
                "output may still be saved if defined in the output parameter."
                "<br/>"
                "Example: <b>dir/*_output.txt</b>"
                "<br/>"
                "In this example data file is saved within the 'dir' "
                "directory. If the job was triggered on 'test.txt' then the "
                "output file would be called 'test_output.txt",
                INPUT_TRIGGER_OUTPUT,
                optional=True
        )
        self.current_form[INPUT_NOTEBOOK_OUTPUT] = \
            self.__create_form_single_input(
                "Notebook output",
                "Notebook output is an optional parameter used to define if "
                "the notebook used for job processing is returned. This is "
                "defined as a path for the notebook to be copied to at job "
                "completion. If it is not provided then the notebook is "
                "destroyed, but other output may still be saved if defined "
                "in the output parameter."
                "<br/>"
                "Example: <b>dir/*_output.ipynb</b>"
                "<br/>"
                "In this example the job notebook is saved within the 'dir' "
                "directory. If the job was triggered on 'test.txt' then the "
                "output notebook would be called 'test_output.ipynb",
                INPUT_NOTEBOOK_OUTPUT,
                optional=True
        )
        self.current_form[INPUT_OUTPUT] = self.__create_form_multi_input(
            "Output",
            "Output data to be saved after job completion. Anything not "
            "saved will be lost. Zero or more files can be copied and should "
            "be expressed in two parts as a variable declaration. The "
            "variable name is the name of the output file within the job, "
            "whilst the value is the file location to which it shall be "
            "copied. In the output string a '*' character can be used to "
            "dynamically create file names, with the * being replaced at "
            "runtime by the triggering files filename. Each output should be "
            "defined in its own text box, and the 'Add output file' button "
            "can be used to create additional text boxes as needed."
            "<br/>"
            "Example: <b>job_output = dir/some_output/*.ipynb</b>"
            "<br/>"
            "In this example, the file 'job_output' is created by the job and "
            "copied to the 'some_output' directory in 'dir'. If 'some_output' "
            "does not already exist it is created. The file will be named "
            "according to the triggering file, and given the '.ipynb' file "
            "extension. If the triggering file was 'sample.txt' then the "
            "output will be called 'sample.ipynb'.",
            INPUT_OUTPUT,
            population_function,
            self.__refresh_edit_form,
            editing=editing,
            display_dict=display_dict,
            apply_function=self.__on_apply_pattern_changes_clicked,
            delete_function=self.__on_delete_pattern_clicked,
            optional=True
        )
        self.current_form[INPUT_RECIPES] = self.__create_form_multi_input(
            "Recipe",
            "Recipe(s) to be used for job definition. These should be recipe "
            "names and may be recipes already defined in the system or "
            "additional ones yet to be added. Each recipe should be defined "
            "in its own text box, and the 'Add recipe' button can be used to "
            "create additional text boxes as needed."
            "<br/>"
            "Example: <b>recipe_1</b>"
            "<br/>"
            "In this example, the recipe 'recipe_1' is used as the definition "
            "of any job processing.",
            INPUT_RECIPES,
            population_function,
            self.__refresh_edit_form,
            editing=editing,
            display_dict=display_dict,
            apply_function=self.__on_apply_pattern_changes_clicked,
            delete_function=self.__on_delete_pattern_clicked,
            extra_text="<br/>Current defined recipes are: ",
            extra_func=self.__list_current_recipes()
        )
        self.current_form[INPUT_VARIABLES] = self.__create_form_multi_input(
            "Variable",
            "Variable(s) accessible to the job at runtime. These are passed "
            "to the job using papermill to run a parameterised notebook. Zero "
            "or more variables can be defined and should be declared as "
            "variable definitions. The variable name will be used as the "
            "variable name within the job notebook, and the vraiable value "
            "will be its value. Any Python data structure can be defined as "
            "long as it can be declared in a single line."
            "<br/>"
            "Example: <b>list_a=[1,2,3]</b>"
            "<br/>"
            "In this example a list of numbers is created and named 'list_a'."
            ,
            INPUT_VARIABLES,
            population_function,
            self.__refresh_edit_form,
            editing=editing,
            display_dict=display_dict,
            apply_function=self.__on_apply_pattern_changes_clicked,
            delete_function=self.__on_delete_pattern_clicked,
            optional=True
        )

    def __populate_new_recipe_form(self, population_function, done_function):
        # TODO update this description

        self.current_form[INPUT_SOURCE] = self.__create_form_single_input(
            "Source",
            "The Jupyter Notebook to be used as a source for the recipe. This "
            "should be expressed as a path to the notebook. Note that if a "
            "name is not provided below then the notebook filename will be "
            "used as the recipe name"
            "<br/>"
            "Example: <b>dir/notebook_1.ipynb</b>"
            "<br/>"
            "In this example this notebook 'notebook_1' in the 'dir' ."
            "directory is imported as a recipe. ",
            INPUT_SOURCE,
            extra_text="<br/>Current defined recipes are: ",
            extra_func=self.__list_current_recipes()
        )
        self.current_form[INPUT_NAME] = self.__create_form_single_input(
            "Name",
            "Optional recipe name. This is used to identify the recipe and so "
            "must be unique. If not provided then the notebook filename is "
            "taken as the name. "
            "<br/>"
            "Example: <b>recipe_1</b>"
            "<br/>"
            "In this example this recipe is given the name 'recipe_1', "
            "regardless of the name of the source notebook.",
            INPUT_NAME,
            optional=True,
            extra_text="<br/>Current defined recipes are: ",
            extra_func=self.__list_current_recipes()
        )

    def __populate_editing_recipe_form(
            self, population_function, editing, display_dict):
        # TODO update this description

        self.current_form[INPUT_NAME] = self.__create_form_single_input(
            "Source",
            "The Jupyter Notebook to be used as a source for the recipe. "
            "This should be expressed as a path to the notebook. Note "
            "that if a name is not provided below then the notebook "
            "filename will be used as the recipe name"
            "<br/>"
            "Example: <b>dir/notebook_1.ipynb</b>"
            "<br/>"
            "In this example this notebook 'notebook_1' in the 'dir' ."
            "directory is imported as a recipe. ",
            INPUT_SOURCE
        )

    def __process_pattern_values(self, values, ignore_conflicts=False):
        # TODO update this description

        try:
            pattern = Pattern(values[INPUT_NAME])
            if not ignore_conflicts:
                if values[INPUT_NAME] in self.patterns:
                    msg = "Pattern name is not valid as another pattern is " \
                          "already registered with that name. "
                    self.__set_feedback(msg)
                    return
            file_name = values[INPUT_TRIGGER_FILE]
            trigger_path = values[INPUT_TRIGGER_PATH]
            trigger_output = values[INPUT_TRIGGER_OUTPUT]
            if trigger_output:
                pattern.add_single_input(file_name,
                                         trigger_path,
                                         output_path=trigger_output)
            else:
                pattern.add_single_input(file_name, trigger_path)
            notebook_return = values[INPUT_NOTEBOOK_OUTPUT]
            if notebook_return:
                pattern.return_notebook(notebook_return)
            for recipe in values[INPUT_RECIPES]:
                pattern.add_recipe(recipe)
            for variable in values[INPUT_VARIABLES]:
                if variable:
                    if '=' in variable:
                        name = variable[:variable.index('=')]
                        value = variable[variable.index('=') + 1:]
                        pattern.add_variable(name, value)
                    else:
                        raise Exception("Variable needs to be declared with a "
                                        "name and a value in the form "
                                        "'name=value', but no '=' is present "
                                        "in %s" % variable)
            for output in values[INPUT_OUTPUT]:
                if output:
                    if '=' in output:
                        name = output[:output.index('=')]
                        value = output[output.index('=') + 1:]
                        pattern.add_output(name, value)
                    else:
                        raise Exception("Output needs to be declared with a "
                                        "name and a value in the form "
                                        "'name=value', but no '=' is present "
                                        "in %s" % output)
            valid, warnings = pattern.integrity_check()
            if valid:
                if pattern.name in self.patterns:
                    word = 'updated'
                    try:
                        pattern.persistence_id = \
                            self.patterns[pattern.name].persistence_id
                    except AttributeError:
                        pass

                else:
                    word = 'created'
                self.patterns[pattern.name] = pattern
                msg = "pattern %s %s. " % (pattern.name, word)
                if warnings:
                    msg += "\n%s" % warnings
                self.__set_feedback(msg)
                self.__update_workflow_visualisation()
                self.__close_form()
                return True
            else:
                msg = "pattern is not valid. "
                if warnings:
                    msg += "\n%s" % warnings
                self.__set_feedback(msg)
                return False
        except Exception as e:
            msg = "Something went wrong with pattern generation. %s" % str(e)
            self.__set_feedback(msg)
            return False

    def __process_recipe_values(self, values, ignore_conflicts=False):
        # TODO update this description

        try:
            source = values[INPUT_SOURCE]
            name = values[INPUT_NAME]

            valid_path(source,
                       'Source',
                       extensions=NOTEBOOK_EXTENSIONS
            )
            if os.path.sep in source:
                filename = \
                    source[source.index('/') + 1:source.index('.')]
            else:
                filename = source[:source.index('.')]
            if not name:
                name = filename
            if not os.path.isfile(source):
                self.__set_feedback("Source %s was not found. " % source)
                return
            if name:
                valid_string(name,
                             'Name',
                             CHAR_UPPERCASE
                             + CHAR_LOWERCASE
                             + CHAR_NUMERIC
                             + CHAR_LINES)
                if not ignore_conflicts:
                    if name in self.recipes:
                        msg = "recipe name is not valid as another recipe " \
                              "is already registered with that name. Please " \
                              "try again using a different name. "
                        self.__set_feedback(msg)
                        return
            self.__set_feedback("Everything seems in order. ")

            with open(source, "r") as read_file:
                notebook = json.load(read_file)
                recipe = create_recipe_dict(notebook, name, source)
                if name in self.recipes:
                    word = 'updated'
                    try:
                        recipe[PERSISTENCE_ID] = \
                            self.recipes[name][PERSISTENCE_ID]
                    except KeyError:
                        pass
                else:
                    word = 'created'
                self.recipes[name] = recipe
                self.__set_feedback("Recipe %s %s. " % (name, word))
            self.__update_workflow_visualisation()
            self.__close_form()
            return True
        except Exception as e:
            self.__set_feedback("Something went wrong with recipe generation. "
                              "%s " % str(e))
            return False

    def __on_new_pattern_clicked(self, button):
        # TODO update this description

        self.__clear_current_form()
        self.__refresh_new_form(
            self.__populate_new_pattern_form, self.__process_pattern_values
        )
        self.__clear_feedback()

    def __on_edit_pattern_clicked(self, button):
        # TODO update this description

        self.__construct_new_edit_form()

    def __on_new_recipe_clicked(self, button):
        # TODO update this description

        self.__clear_current_form()
        self.__refresh_new_form(
            self.__populate_new_recipe_form, self.__process_recipe_values
        )
        self.__clear_feedback()

    def __on_edit_recipe_clicked(self, button):
        # TODO update this description

        self.__clear_current_form()
        self.__refresh_edit_form(
            RECIPE_NAME,
            self.recipes,
            self.__populate_editing_recipe_form,
            self.__on_apply_recipe_changes_clicked,
            self.__on_delete_recipe_clicked
        )
        self.__clear_feedback()

    def __refresh_new_form(
            self, population_function, done_function, wait=False):
        # TODO update this description

        if self.current_form:
            self.current_old_values = {}
            for key in self.current_form_rows.keys():
                self.current_old_values[key] = self.current_form_rows[key]
        self.current_form = {}
        # if self.displayed_form:
        #     self.displayed_form.close()
        self.display_area.clear_output(wait=wait)

        population_function(population_function, done_function)

        items = []
        for key in self.current_form.keys():
            items.append(self.current_form[key])

        self.current_form["done_button"] = widgets.Button(
            value=False,
            description="Done",
            disabled=False,
            button_style='',
            tooltip='Here is a tooltip for this button'
        )

        def done_button_click(button):
            values = {}
            for key in self.current_form_rows.keys():
                row = self.current_form_rows[key]
                if isinstance(row, list):
                    values_list = []
                    for element in row:
                        values_list.append(element.value)
                    values[key] = values_list
                else:
                    values[key] = self.current_form_rows[key].value

            done_function(values)

        self.current_form["done_button"].on_click(done_button_click)

        self.current_form["cancel_button"] = widgets.Button(
            value=False,
            description="Cancel",
            disabled=False,
            button_style='',
            tooltip='Here is a tooltip for this button'
        )

        def cancel_button_click(button):
            if isinstance(self.displayed_form, widgets.VBox):
                self.__close_form()
                self.current_old_values = {}
                for text_key in self.current_form_rows.keys():
                    self.current_old_values[text_key] = \
                        self.current_form_rows[text_key]
                self.__clear_feedback()

        self.current_form["cancel_button"].on_click(cancel_button_click)

        bottom_row_items = [
            self.current_form["done_button"],
            self.current_form["cancel_button"]
        ]
        bottom_row = widgets.HBox(bottom_row_items)
        items.append(bottom_row)

        self.displayed_form = widgets.VBox(items)

        with self.display_area:
            form_id = display(self.displayed_form, display_id=True)

    def __refresh_edit_form(
            self, editing, display_dict, population_function, apply_function,
            delete_function, wait=False, default=None):
        # TODO update this description

        if self.current_form:
            self.current_old_values = {}
            for key in self.current_form_rows.keys():
                self.current_old_values[key] = self.current_form_rows[key]
        self.current_form = {}
        # if self.displayed_form:
        #     self.displayed_form.close()
        self.display_area.clear_output(wait=wait)
        self.editing_area = None

        options = []
        for key in display_dict:
            options.append(key)

        dropdown = widgets.Dropdown(
            options=options,
            value=None,
            description="%s: " % editing,
            disabled=False,
        )

        def on_dropdown_select(change):
            if change['type'] == 'change' and change['name'] == 'value':
                to_edit = display_dict[change['new']]
                self.editing = (editing, to_edit)

                # update row counts
                if isinstance(to_edit, Pattern) and not default:
                    pattern = to_edit
                    extra_outputs = []
                    for out in pattern.outputs.keys():
                        if out != DEFAULT_JOB_NAME \
                                and out != pattern.input_file:
                            extra_outputs.append(out)
                    if len(extra_outputs) > 1:
                        self.current_form_line_counts[INPUT_OUTPUT] = \
                            len(extra_outputs) - 1
                    else:
                        self.current_form_line_counts[INPUT_OUTPUT] = 0

                    if len(pattern.recipes) > 1:
                        self.current_form_line_counts[INPUT_OUTPUT] = \
                            len(pattern.recipes) - 1
                    else:
                        self.current_form_line_counts[INPUT_OUTPUT] = 0

                    extra_variables = []
                    for variable in pattern.variables.keys():
                        if variable != pattern.input_file and variable != \
                                DEFAULT_JOB_NAME:
                            extra_variables.append(variable)
                    if len(extra_variables) > 1:
                        self.current_form_line_counts[INPUT_VARIABLES] = \
                            len(extra_variables) - 1
                    else:
                        self.current_form_line_counts[INPUT_VARIABLES] = 0

                if not default:
                    self.__refresh_edit_form(
                        editing,
                        display_dict,
                        population_function,
                        apply_function,
                        delete_function,
                        wait=False,
                        default=to_edit
                    )

        dropdown.observe(on_dropdown_select)

        top_row_items = [
            dropdown
        ]
        top_row = widgets.HBox(top_row_items)

        items = [
            top_row
        ]

        self.displayed_form = widgets.VBox(items)

        with self.display_area:
            form_id = display(self.displayed_form, display_id=True)

        # TODO fix this to distinguish between patterns and recipes
        if default:
            if isinstance(default, Pattern):
                default_name = default.name
            else:
                default_name = default[NAME]
            if default_name in options:
                dropdown.value = default_name
                self.__editor(
                    population_function,
                    editing,
                    display_dict,
                    apply_function,
                    delete_function
                )
                default = None

    def __editor(
            self, population_function, editing, display_dict, apply_function,
            delete_function):
        # TODO update this description

        if not self.editing_area:
            population_function(population_function, editing, display_dict)

            items = []
            for key in self.current_form.keys():
                items.append(self.current_form[key])

            apply = widgets.Button(
                value=False,
                description="Apply Changes",
                disabled=False,
                button_style='',
                tooltip='TODO'
            )
            apply.on_click(apply_function)

            delete = widgets.Button(
                value=False,
                description="Delete",
                disabled=False,
                button_style='',
                tooltip='TODO'
            )
            delete.on_click(delete_function)

            cancel = widgets.Button(
                value=False,
                description="Cancel",
                disabled=False,
                button_style='',
                tooltip='TODO'
            )
            cancel.on_click(self.__on_cancel_clicked)

            button_items = [
                apply,
                delete,
                cancel
            ]
            button_row = widgets.HBox(button_items)
            self.current_form['buttons'] = button_row

            items.append(button_row)

            self.editing_area = widgets.VBox(items)

            with self.display_area:
                display(self.editing_area)

        if isinstance(self.editing[1], Pattern):
            pattern = self.editing[1]

            self.current_form_rows[INPUT_TRIGGER_FILE].value = \
                pattern.input_file

            if pattern.trigger_paths:
                # TODO note this deletes any extra paths as currently only
                #  one at a time. change this
                self.current_form_rows[INPUT_TRIGGER_PATH].value = \
                    pattern.trigger_paths[0]

            if pattern.input_file in pattern.outputs.keys():
                self.current_form_rows[INPUT_TRIGGER_OUTPUT].value = \
                    pattern.outputs[pattern.input_file]

            if DEFAULT_JOB_NAME in pattern.outputs.keys():
                self.current_form_rows[INPUT_NOTEBOOK_OUTPUT].value = \
                    pattern.outputs[DEFAULT_JOB_NAME]

            extra_outputs = []
            for out in pattern.outputs.keys():
                if out != DEFAULT_JOB_NAME and out != pattern.input_file:
                    extra_outputs.append(out)
            if extra_outputs:
                for i in range(0, len(self.current_form_rows[INPUT_OUTPUT])):
                    if i < len(extra_outputs):
                        self.current_form_rows[INPUT_OUTPUT][i].value = \
                            "%s=%s" % (extra_outputs[i],
                                       pattern.outputs[extra_outputs[i]])

            for i in range(0, len(self.current_form_rows[INPUT_RECIPES])):
                if i < len(pattern.recipes):
                    self.current_form_rows[INPUT_RECIPES][i].value = \
                        "%s" % pattern.recipes[i]

            extra_variables = []
            for variable in pattern.variables.keys():
                if variable != pattern.input_file and variable != \
                        DEFAULT_JOB_NAME:
                    extra_variables.append(variable)
            if extra_variables:
                for i in range(0, len(self.current_form_rows[INPUT_VARIABLES])):
                    if i < len(extra_variables):
                        self.current_form_rows[INPUT_VARIABLES][i].value = \
                            "%s=%s" % (extra_variables[i],
                                       pattern.variables[extra_variables[i]])
        else:
            recipe = self.editing[1]
            self.current_form_rows[INPUT_SOURCE].value = recipe[SOURCE]

    def __on_apply_recipe_changes_clicked(self, button):
        # TODO update this description

        values = {
            INPUT_NAME: self.editing[1][NAME],
            INPUT_SOURCE: self.current_form[INPUT_SOURCE].value
        }
        if self.__process_recipe_values(values, ignore_conflicts=True):
            self.__done_editing()

    def __on_delete_recipe_clicked(self, button):
        # TODO update this description

        to_delete = self.editing[1][NAME]
        if to_delete in self.recipes.keys():
            self.recipes.pop(to_delete)
        self.__set_feedback("Recipe %s deleted. " % to_delete)
        self.__update_workflow_visualisation()
        self.__done_editing()

    def __on_apply_pattern_changes_clicked(self, button):
        # TODO update this description

        values = {
            INPUT_NAME: self.editing[1].name
        }
        for key in self.current_form_rows.keys():
            row = self.current_form_rows[key]
            if isinstance(row, list):
                values_list = []
                for element in row:
                    values_list.append(element.value)
                values[key] = values_list
            else:
                values[key] = self.current_form_rows[key].value
        if self.__process_pattern_values(values, ignore_conflicts=True):
            self.__done_editing()

    def __on_delete_pattern_clicked(self, button):
        # TODO update this description

        to_delete = self.editing[1].name
        if to_delete in self.patterns.keys():
            self.patterns.pop(to_delete)
        self.__set_feedback("Pattern %s deleted. " % to_delete)
        self.__update_workflow_visualisation()
        self.__done_editing()

    def __on_cancel_clicked(self, button):
        # TODO update this description

        if isinstance(self.displayed_form, widgets.VBox):
            self.__done_editing()
            self.__clear_feedback()

    def __done_editing(self):
        # TODO update this description

        self.__close_form()
        self.editing_area = None
        self.editing = None

    def __make_help_button(self, help_text, extra_text, extra_func):
        # TODO update this description

        help_button = widgets.Button(
            value=False,
            description="Toggle help",
            disabled=False,
            button_style='',
            tooltip='Here is a tooltip for this button'
        )
        help_html = widgets.HTML(
            value=""
        )
        def help_button_click(button):
            if help_html.value is "":
                message = help_text
                if extra_text:
                    message += extra_text
                if extra_func:
                    message += extra_func
                help_html.value = message
            else:
                help_html.value = ""

        help_button.on_click(help_button_click)

        return help_button, help_html

    def __create_form_single_input(
            self, text, help_text, key, extra_text=None, extra_func=None,
            optional=False):
        # TODO update this description

        msg = text
        if optional:
            msg += " (optional)"
        label = widgets.Label(
            value="%s: " % msg
        )

        input = widgets.Text()
        if key in self.current_old_values:
            input.value = self.current_old_values[key].value
            self.current_old_values.pop(key, None)

        # self.current_form[key] = input
        self.current_form_rows[key] = input

        help_button, help_text = self.__make_help_button(help_text,
                                                         extra_text=extra_text,
                                                         extra_func=extra_func)

        top_row_items = [
            label,
            input,
            help_button
        ]

        top_row = widgets.HBox(top_row_items)

        items = [
            top_row,
            help_text
        ]

        input_widget = widgets.VBox(items)
        return input_widget

    def __create_form_multi_input(
            self, text, help_text, key, population_function, refresh_function,
            done_function=None, display_dict=None, editing=None,
            apply_function=None, delete_function=None, extra_text=None,
            extra_func=None, optional=False):
        # TODO update this description

        msg = text
        if optional:
            msg += " (optional)"
        label = widgets.Label(
            value="%s(s): " % msg
        )
        input = widgets.Text()

        help_button, help_text = self.__make_help_button(help_text,
                                                         extra_text=extra_text,
                                                         extra_func=extra_func)

        input_old_values = []
        if key in self.current_old_values:
            input_old_values = self.current_old_values[key]
        if input_old_values:
            input.value = input_old_values[0].value
            del input_old_values[0]

        self.current_form_rows[key] = [input]

        add_button = widgets.Button(
            value=False,
            description="Add %s" % text.lower(),
            disabled=False,
            button_style='',
            tooltip='Here is a tooltip for this button'
        )

        def add_button_click(button):
            if key in self.current_form_line_counts.keys():
                self.current_form_line_counts[key] += 1
            else:
                self.current_form_line_counts[key] = 1
            if refresh_function == self.__refresh_new_form:
                self.__refresh_new_form(population_function,
                                       done_function,
                                       wait=True)
            elif refresh_function == self.__refresh_edit_form:
                self.__refresh_edit_form(editing,
                                        display_dict,
                                        population_function,
                                        apply_function,
                                        delete_function,
                                        wait=True,
                                        default=self.editing[1])

        add_button.on_click(add_button_click)

        remove_button = widgets.Button(
            value=False,
            description="Remove %s" % text.lower(),
            disabled=False,
            button_style='',
            tooltip='Here is a tooltip for this button'
        )

        def remove_button_click(button):
            if key in self.current_form_line_counts.keys():
                if self.current_form_line_counts[key] > 0:
                    self.current_form_line_counts[key] -= 1
            if refresh_function == self.__refresh_new_form:
                self.__refresh_new_form(population_function,
                                       done_function,
                                       wait=True)
            elif refresh_function == self.__refresh_edit_form:
                self.__refresh_edit_form(editing,
                                        display_dict,
                                        population_function,
                                        apply_function,
                                        delete_function,
                                        wait=True,
                                        default=self.editing[1])

        if key in self.current_form_line_counts.keys():
            if self.current_form_line_counts[key] == 0:
                remove_button.disabled = True
        else:
            remove_button.disabled = True

        remove_button.on_click(remove_button_click)

        top_row_items = [
            label,
            input,
            help_button
        ]
        top_row = widgets.HBox(top_row_items)

        extra_rows = []

        if key in self.current_form_line_counts.keys():
            extra_rows_count = self.current_form_line_counts[key]
            for x in range(0, extra_rows_count):
                extra_input = widgets.Text()
                if input_old_values:
                    extra_input.value = input_old_values[0].value
                    del input_old_values[0]
                extra_row_items = [
                    extra_input
                ]
                extra_row = widgets.HBox(extra_row_items)
                extra_rows.append(extra_row)

                self.current_form_rows[key].append(extra_input)

                # if key in form:
                #     form[key].append(extra_input)

        if key in self.current_old_values:
            self.current_old_values.pop(key, None)

        bottom_row_items = [
            add_button,
            remove_button
        ]
        bottom_row = widgets.HBox(bottom_row_items)

        form_items = [
            top_row,
        ]
        for row in extra_rows:
            form_items.append(row)
        form_items.append(bottom_row)
        form_items.append(help_text)

        form_row = widgets.VBox(form_items)

        return form_row

    def __on_import_from_vgrid_clicked(self, button):
        # TODO update this description

        self.__close_form()
        self.__clear_feedback()
        self.__import_from_vgrid()

    def __import_from_vgrid(self, confirm=True):
        self.__set_feedback("Importing workflow from Vgrid. This may take a "
                            "few seconds.")

        try:
            vgrid, _, response, _ = vgrid_json_call('read',
                                                    'any',
                                                    print_feedback=False)
        except LookupError as error:
            self.__set_feedback(error)
            self.__enable_top_buttons()
            return
        except Exception as err:
            self.__set_feedback(str(err))
            self.__enable_top_buttons()
            return
        self.__clear_feedback()
        response_patterns = {}
        response_recipes = {}
        if VGRID_WORKFLOWS_OBJECT in response:
            for response_object in response[VGRID_WORKFLOWS_OBJECT]:
                if response_object[OBJECT_TYPE] == VGRID_PATTERN_OBJECT_TYPE:
                    response_patterns[response_object[NAME]] = response_object
                elif response_object[OBJECT_TYPE] == VGRID_RECIPE_OBJECT_TYPE:
                    response_recipes[response_object[NAME]] = response_object

            args = {
                PATTERNS: response_patterns,
                RECIPES: response_recipes
            }
            if confirm:
                self.__add_to_feedback("Found %s pattern(s) from Vgrid %s: %s "
                                       % (len(response_patterns), vgrid,
                                          list(response_patterns.keys())))
                self.__add_to_feedback("Found %s recipe(s) from Vgrid %s: %s "
                                       % (len(response_recipes), vgrid,
                                          list(response_recipes.keys())))

                self.__add_to_feedback("Import these patterns and recipes "
                                       "into local memory? This will "
                                       "overwrite any patterns or recipes "
                                       "currently in memory that share the "
                                       "same name. ")

                self.__create_confirmation_buttons(
                    self.__import_workflow,
                    args,
                    "Confirm Import",
                    "Cancel Import",
                    "Import canceled. No local data has been changed. "
                )
            else:
                self.__import_workflow(**args)

        elif response[OBJECT_TYPE] == VGRID_ERROR_TYPE:
            self.__set_feedback(response[VGRID_TEXT_TYPE])
        else:
            print('Got an unexpected response')
            print("Unexpected response: {}".format(response))
        self.__enable_top_buttons()

    def __import_workflow(self, **kwargs):
        response_patterns = kwargs.get(PATTERNS, None)
        response_recipes = kwargs.get(RECIPES, None)

        self.mig_imports = {
            PATTERNS: {},
            RECIPES: {}
        }
        overwritten_patterns = []
        overwritten_recipes = []
        for key, pattern in response_patterns.items():
            if key in self.patterns:
                overwritten_patterns.append(key)
            new_pattern = Pattern(pattern)
            self.patterns[key] = new_pattern
            try:
                self.mig_imports[PATTERNS][new_pattern.persistence_id] = \
                    deepcopy(new_pattern)
            except AttributeError:
                pass
        for key, recipe in response_recipes.items():
            if key in self.recipes:
                overwritten_recipes.append(key)
            self.recipes[key] = recipe
            try:
                self.mig_imports[RECIPES][recipe[PERSISTENCE_ID]] = \
                    deepcopy(recipe)
            except AttributeError:
                pass

        msg = "Imported %s patterns and %s recipes. " \
              % (len(response_patterns), len(response_recipes))
        if overwritten_patterns:
            msg += "<br/>Overwritten patterns: %s " % overwritten_patterns
        if overwritten_recipes:
            msg += "<br/>Overwritten recipes: %s " % overwritten_recipes
        self.__set_feedback(msg)
        self.__update_workflow_visualisation()
        self.__close_form()

    def __count_calls(self, calls, operation, type):
        count = [i[2][NAME] for i in calls
                 if i[0] == operation and i[1] == type]
        return count

    def __on_export_to_vgrid_clicked(self, button):
        # TODO update this description

        self.__close_form()
        self.__clear_feedback()

        calls = []
        pattern_ids = []
        for _, pattern in self.patterns.items():
            attributes = {
                NAME: pattern.name,
                INPUT_FILE: pattern.input_file,
                TRIGGER_PATHS: pattern.trigger_paths,
                OUTPUT: pattern.outputs,
                RECIPES: pattern.recipes,
                VARIABLES: pattern.variables
            }
            try:
                if pattern.persistence_id:
                    attributes[PERSISTENCE_ID] = pattern.persistence_id
                    pattern_ids.append(pattern.persistence_id)
            except AttributeError:
                pass
            try:
                operation = None
                if PERSISTENCE_ID in attributes:
                    if self.patterns[pattern.name] != \
                            self.mig_imports[PATTERNS][pattern.persistence_id]:
                        operation = VGRID_UPDATE

                else:
                    operation = VGRID_CREATE
                if operation:
                    calls.append(
                        (
                            operation,
                            VGRID_PATTERN_OBJECT_TYPE,
                            attributes,
                            False,
                            pattern
                        )
                    )
            except LookupError as error:
                self.__set_feedback(error)
                return

        recipe_ids = []
        for _, recipe in self.recipes.items():
            try:
                attributes = {
                    NAME: recipe[NAME],
                    RECIPE: recipe[RECIPE],
                    SOURCE: recipe[SOURCE]
                }
                try:
                    if recipe[PERSISTENCE_ID]:
                        attributes[PERSISTENCE_ID] = recipe[PERSISTENCE_ID]
                        recipe_ids.append(recipe[PERSISTENCE_ID])
                except KeyError:
                    pass
                operation = None
                if PERSISTENCE_ID in attributes:
                    if self.recipes[recipe[NAME]] != \
                            self.mig_imports[RECIPES][recipe[PERSISTENCE_ID]]:
                        operation = VGRID_UPDATE
                else:
                    operation = VGRID_CREATE
                if operation:
                    calls.append(
                        (
                            operation,
                            VGRID_RECIPE_OBJECT_TYPE,
                            attributes,
                            False,
                            recipe
                        )
                    )
            except LookupError as error:
                self.__set_feedback(error)
                return

        operation = VGRID_DELETE
        for id, name in self.mig_imports[PATTERNS].items():
            if id not in pattern_ids:
                attributes = {
                    PERSISTENCE_ID: id,
                    NAME: name
                }
                calls.append(
                    (
                        operation,
                        VGRID_PATTERN_OBJECT_TYPE,
                        attributes,
                        False
                    )
                )
        for id, name in self.mig_imports[RECIPES].items():
            if id not in recipe_ids:
                attributes = {
                    PERSISTENCE_ID: id,
                    NAME: name
                }
                calls.append(
                    (
                        operation,
                        VGRID_RECIPE_OBJECT_TYPE,
                        attributes,
                        False
                    )
                )
        self.__enable_top_buttons()

        if not calls:
            self.__set_feedback("No patterns or recipes have been created, "
                                "updated or deleted so there is nothing to "
                                "export to the Vgrid")
            self.__enable_top_buttons()
            return

        operation_combinations = [
            (VGRID_CREATE, VGRID_PATTERN_OBJECT_TYPE),
            (VGRID_CREATE, VGRID_RECIPE_OBJECT_TYPE),
            (VGRID_UPDATE, VGRID_PATTERN_OBJECT_TYPE),
            (VGRID_UPDATE, VGRID_RECIPE_OBJECT_TYPE),
            (VGRID_DELETE, VGRID_PATTERN_OBJECT_TYPE),
            (VGRID_DELETE, VGRID_RECIPE_OBJECT_TYPE),
        ]

        for operation in operation_combinations:
            relevant_calls = \
                self.__count_calls(calls, operation[0], operation[1])

            if relevant_calls:
                self.__add_to_feedback("Will %s %s %s: %s. "
                                       % (operation[0], len(relevant_calls),
                                          operation[1], relevant_calls))

        # Strip names from delete calls. They were only included for feedback
        # purposes and may complicate mig operations

        self.__create_confirmation_buttons(
            self.__export_workflow,
            {
                'calls': calls
            },
            "Confirm Export",
            "Cancel Export",
            "Export canceled. No VGrid data has been changed. "
        )

    def __export_workflow(self, **kwargs):
        self.__clear_feedback()
        calls = kwargs.get('calls', None)
        for call in calls:
            try:
                operation = call[0]
                object_type = call[1]
                vgrid, _, response, _ = vgrid_json_call(
                    operation, object_type, attributes=call[2],
                    print_feedback=call[3]
                )
                if 'text' in response and len(call) == 5:
                    if operation == VGRID_CREATE:
                        persistence_id = response['text']
                        if object_type == VGRID_PATTERN_OBJECT_TYPE:
                            pattern = call[4]
                            pattern.persistence_id = persistence_id
                            self.__add_to_feedback("Created pattern %s" %
                                                   pattern.name)
                        elif object_type == VGRID_RECIPE_OBJECT_TYPE:
                            recipe = call[4]
                            recipe[PERSISTENCE_ID] = persistence_id
                            self.__add_to_feedback("Created recipe %s" %
                                                   recipe[NAME])

                    else:
                        feedback = response['text'].replace('\n', '<br/>')
                        self.__add_to_feedback(feedback)
                if 'error_text' in response:
                    feedback = response['error_text'].replace('\n', '<br/>')
                    self.__add_to_feedback(feedback)

            except Exception as err:
                self.__set_feedback(err)
        self.__close_form()

    def __create_confirmation_buttons(
            self, confirmation_function, confirmation_args, confirm_text,
            cancel_text, cancel_feedback):
        confirm_button = widgets.Button(
            value=False,
            description=confirm_text,
            disabled=False,
            button_style='',
            tooltip='Here is a tooltip for this button'
        )

        def confirm_button_click(button):
            confirmation_function(**confirmation_args)

        confirm_button.on_click(confirm_button_click)

        cancel_button = widgets.Button(
            value=False,
            description=cancel_text,
            disabled=False,
            button_style='',
            tooltip='Here is a tooltip for this button'
        )

        def cancel_button_click(button):
            self.__set_feedback(cancel_feedback)
            self.__close_form()

        cancel_button.on_click(cancel_button_click)

        buttons_list = [
            confirm_button,
            cancel_button
        ]

        confirmation_buttons = widgets.HBox(buttons_list)

        with self.display_area:
            display(confirmation_buttons, display_id=True)

    def __add_to_feedback(self, to_add):
        # TODO update this description

        if self.feedback.value:
            self.feedback.value += "<br/>"
        self.feedback.value += to_add

    def __set_feedback(self, to_set):
        # TODO update this description

        self.feedback.value = to_set

    def __clear_feedback(self):
        # TODO update this description

        self.feedback.value = ""

    def __close_form(self):
        # TODO update this description

        self.displayed_form = None
        self.display_area.clear_output()
        self.__enable_top_buttons()
        self.__clear_current_form()

    def __clear_current_form(self):
        # TODO update this description

        self.current_form = {}
        self.current_old_values = {}
        self.current_form_rows = {}
        self.current_form_line_counts = {}

    def __update_workflow_visualisation(self):
        # TODO update this description

        try:
            self.workflow = build_workflow_object(
                self.patterns,
                self.recipes
            )
        except:
            self.workflow = {}
        visualisation = self.__get_workflow_visualisation(
            self.patterns,
            self.recipes,
            self.workflow
        )
        self.visualisation_area.clear_output(wait=True)

        with self.visualisation_area:
            display(visualisation)

    def __set_node_dict(self, pattern):
        # TODO update this description

        node_dict = {
            'label': pattern.name,
            'Name': pattern.name,
            'Recipe(s)': str(pattern.recipes),
            'Trigger Path(s)': str(pattern.trigger_paths),
            'Outputs(s)': str(pattern.outputs),
            'Input File': pattern.input_file,
            'Variable(s)': str(pattern.variables),
            'shape': 'circle',
            'shape_attrs': {'r': 30}
        }
        return node_dict

    def __get_index(self, pattern, nodes):
        # TODO update this description

        for index in range(0, len(nodes)):
            if nodes[index]['Name'] == pattern:
                return index
        return -1

    def __visualisation_element_click(self, graph, element):
        # TODO update this description

        # pattern = self.patterns[element['data']['label']]
        # self.construct_new_edit_form(default=pattern)
        pass

    def __construct_new_edit_form(self, default=None):
        # TODO update this description

        self.__clear_current_form()
        self.__refresh_edit_form(
            PATTERN_NAME,
            self.patterns,
            self.__populate_editing_pattern_form,
            self.__on_apply_pattern_changes_clicked,
            self.__on_delete_pattern_clicked,
            default=default
        )
        self.__clear_feedback()

    def __get_workflow_visualisation(self, patterns, recipes, workflow):
        # TODO update this description

        fig_layout = widgets.Layout(width='900px', height='500px')

        pattern_display = []

        for pattern in workflow.keys():
            pattern_display.append(self.__set_node_dict(patterns[pattern]))

        link_display = []
        colour_display = [RED] * len(pattern_display)

        for pattern, descendants in workflow.items():
            pattern_index = self.__get_index(pattern, pattern_display)
            if pattern_has_recipes(patterns[pattern], recipes):
                colour_display[pattern_index] = GREEN
            else:
                colour_display[pattern_index] = RED
            for descendant in descendants:
                descendant_index = \
                    self.__get_index(descendant, pattern_display)

                link_display.append({
                    'source': pattern_index,
                    'target': descendant_index
                })

        graph = Graph(
            node_data=pattern_display,
            link_data=link_display,
            charge=-400,
            colors=colour_display
        )
        tooltip = Tooltip(
            fields=[
                'Name',
                'Recipe(s)',
                'Trigger Path(s)',
                'Outputs(s)',
                'Input File',
                'Variable(s)'
            ],
            # formats=['', '', '']
        )
        graph.tooltip = tooltip
        graph.on_element_click(self.__visualisation_element_click)

        return Figure(marks=[graph], layout=fig_layout)

    def display_widget(self):
        # TODO update this
        """Displays a widget for workflow defitions. Can optionally take a
        predefined workflow as input"""

        workflow_image = [self.visualisation_area]
        image_row = widgets.HBox(workflow_image)

        button_row_items = [self.new_pattern_button,
                            self.edit_pattern_button,
                            self.new_recipe_button,
                            self.edit_recipe_button,
                            self.import_from_vgrid_button,
                            self.export_to_vgrid_button]
        button_row = widgets.HBox(button_row_items)

        feedback_items = [
            self.feedback
        ]
        feedback_row = widgets.HBox(feedback_items)

        display_items = [
            self.display_area
        ]
        display_row = widgets.HBox(display_items)

        widget = widgets.VBox(
            [
                image_row,
                button_row,
                display_row,
                feedback_row
            ]
        )
        self.__enable_top_buttons()
        return widget
