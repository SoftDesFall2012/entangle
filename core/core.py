class core:

    def __init__(self):
        self.txt = open('txt_output.txt').read()

        self.buffer = open('buffer_output.txt').read()
        self.buffer = self.buffer.strip('[]')
        self.buffer = self.buffer.split(',')

        self.header = open('header.txt').read()

        self.cv_list = []
        self. lv_list = []

        self.count = []

    def indexer(self):

        strip_buffer = self.buffer

        # Split the buffer output into smaller and more usable lists.
        font_index = strip_buffer.index("'|'") #make sure jong csvs the '|'
        font_list = strip_buffer[:font_index]

        del strip_buffer[:font_index+1]

        cv_index = strip_buffer.index("'|'")
        cv_list = strip_buffer[:cv_index]

        del strip_buffer[:cv_index+1]

        lv_list = strip_buffer

        # Clean up the lists a bit.

        for i in range(len(cv_list)/6):
            if i == 0:
                del cv_list[i]
            else:
                del cv_list[i*6-i]
        for i in range(len(lv_list)/7):
            if i == 0:
                del lv_list[i]
            else:
                del lv_list[i*7-i]

        self.cv_list = cv_list
        self.lv_list = lv_list

    def do_header_inject(self):

        print len(self.lv_list)/6
        header = self.header

        n_lv = len(self.lv_list)/6

        for i in range(n_lv):
            self.count.append(i)

            word1 = str(self.lv_list[1+(i*6)])
            word2 = str(self.lv_list[0+(i*6)])

            word1 = word1.lstrip(' ["u')
            word2 = word2.lstrip(' ["u')
            word1 = word1.strip("' ")
            word2 = word2.strip("' ")
            word1 = word1.replace(' ','')
            word2 = word2.replace(' ','')

            n_value = str(self.lv_list[3+(i*6)])

            n_value = n_value.strip("' ")

            function_value = str(self.lv_list[2+(i*6)])

            function_value = function_value.strip("' ")

            header += '\n\t<script type = "text/javascript">\n'
            header += '\t\tfunction setUpTangle () {\n'
            header += '\t\t\tvar element = document.getElementById("'+str(i)+'");\n'
            header += '\t\t\tvar tangle = new Tangle(element, {\n'
            header += '\t\t\t\tinitialize: function() {\n'
            header += '\t\t\t\t\tthis.'+word1+' = 5;\n'
            header += '\t\t\t\t\tthis.'+word2+'Per'+word1+' = '+n_value+';\n'
            header += '\t\t\t\t},\n'
            header += '\t\t\t\tupdate: function () {\n'
            header += '\t\t\t\t\tthis.'+word2+' = this.'+word1+function_value+'this.'+word2+'Per'+word1+';\n'
            header += '\t\t\t\t}\n'
            header += '\t\t\t}};\n'
            header += '\t\t}\n'
            header += '\t</script>\n\n'

        header += '</head>'

        self.header = header

            print word1
            print word2
            print header

    def main(self):
        core.indexer(self)
        print core.do_header_inject(self)

core().main()