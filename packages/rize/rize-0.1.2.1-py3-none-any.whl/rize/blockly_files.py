import rize

class toolbox_creator:
    def __init__(self, name_toolbox, color_inputs, color_outputs):
        """Creates a new blockly toolbox
            
            Parameters
            ----------
            name_toolbox: string
                USe this parameter to set the Javascript variable name
        """

        self.color_inputs = color_inputs
        self.color_outputs = color_outputs
        self.categories = {} # This variabel saves the XML definitions of the blocks in a string 
        self.name_toolbox = name_toolbox
    
    def add_xml_block(self,block_name,category):
        """ Add a new block definition to the toolbox and set the category
            
            Parameters
            ----------

            block_name : string 
                Name of the block
            category : string 
                Category of the block
        """

        if category in self.categories:
            # Concatenate a block in the XML definition (in a string) of the category
            self.categories[category] = self.categories[category] +  self.name_toolbox + " +='    <block type=" +'"'+ str(block_name) +'"' + "></block>';\n"
        else:
            # Start the XML definition (in a string) of a category
            self.categories[category] =  self.name_toolbox + " +='    <block type=" +'"'+ str(block_name) +'"' + "></block>';\n"
            

    def __add_category(self, category_name, color = "#F62459"):
        category_name = category_name.replace("_", " ")
        value =  self.name_toolbox + " += '" +  '<category name="' + str(category_name) + '"' + ' colour="' +  color + '"' + """>'\n"""
        return value

    def get_blocks(self):

        outputs = self.__add_category("Robot actions",self.color_outputs ) + self.categories["output"] +  self.name_toolbox + """ += '  </category>';\n"""
        inputs = self.__add_category("Event inputs",self.color_inputs ) + self.categories["input"] +  self.name_toolbox + """ += '  </category>';\n"""

        return outputs, inputs


class blockly_files:
    """
        Write and save the javascript files needed to define a blockly enviroment

        Parameters
        ----------

        name_files: string
            name of the blockly files that will be generated (block definition and code generator)
        name_toolbox: string
            name of the toolbox file that will be generated
    """
    def __init__(self, name_files, name_toolbox, path_blocks = "", color_input = "#009688" , color_output = "#2196f3"):

        self.path_blocks = path_blocks
        # -------------- Files to configurate ---------------
        # Blocks files
        self.file_b = open(path_blocks + "/blockly/blocks/" + name_files + ".js","w")
        # Generator files
        self.file_g = open(path_blocks + "/blockly/generators/python/" + name_files + ".js","w")
        # Toolbox file
        self.file_input = open( "toolbox/" + "blocks_inputs.js","w") 
        # Toolbox file
        self.file_output = open( "toolbox/" + "blocks_outputs.js","w") 
        self.database={}

        # --------------- Definition of primitives ------------
        # Define start of blocks file
        blocks_init = "goog.provide('Blockly.Blocks." + name_files + "');\ngoog.require('Blockly.Blocks');\n"
        # Define start of generator file
        generator_init = "'use strict'\ngoog.provide('Blockly.Python."+ name_files +"');\ngoog.require('Blockly.Python');"
        
        self.file_b.write(blocks_init)
        self.file_g.write(generator_init)

        # Define toobox creator file
        self.toolbox = toolbox_creator(name_toolbox, color_input, color_output)


    def add_code_generator(self,code):
        """ Add the code that will be generated the a block
        
            Parameters
            ----------

            code:string
                javascript and python code to be added
        """
        self.file_g.write("\n\n") 
        self.file_g.write(code)

        
    def add_block_definition(self,block):
        """ Add the javascript block definition
        
            Parameters
            ----------

            block:string
                javascript that define the design, inputs and outputs of a block
        """

        self.file_b.write("\n\n") 
        self.file_b.write(block)

    def add_toolbox_xml(self,name,block_type):
        """ This function add a new block description to a XML file that define the blockly toolbox.
        """
        self.toolbox.add_xml_block(name,block_type)

    def add_database(self, name_file, data):
        """ Add database values for each primitive
        
            Parameters
            ----------

            name_file: string
                Name of the file that describes the primitive

            data:dictionary
                dictionary with the description of the primitive
        """

        self.database[name_file] = data        

    def close_files(self):
        """ This function close the files created, code generators, toolbox and blocks.
        """
       
        out, inp = self.toolbox.get_blocks()
        self.file_output.write(out)
        self.file_input.write(inp)
        self.file_output.close()
        self.file_input.close()
        
        self.file_b.close()
        self.file_g.close()
        rize.onSaveJSON("databases", "primitives", self.database)
       

