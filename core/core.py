class core:

    def __init__(self):
        self.txt = open('txt_output.txt').read()
        self.txt = self.txt.strip('[]')


        self.buffer = open('buffer_output.txt').read()
        self.buffer = self.buffer.strip('[]')
        self.buffer = self.buffer.split(',')

        self.header = open('header.txt').read()
        self.body = ''

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

        header = self.header

        n_lv = len(self.lv_list)/6

        for i in range(n_lv):


            word1 = str(self.lv_list[1+(i*6)])
            word2 = str(self.lv_list[0+(i*6)])

            word1 = word1.lstrip(' ["u')
            word2 = word2.lstrip(' ["u')
            word1 = word1.strip("' ")
            word2 = word2.strip("' ")
            self.count.append([str(i), word1, word2])
            word1 = word1.replace(' ','')
            word2 = word2.replace(' ','')

            n_value = str(self.lv_list[3+(i*6)])

            n_value = n_value.strip("' ")

            function_value = str(self.lv_list[2+(i*6)])

            function_value = function_value.strip("' ")

            header += '\n\n\t<script type = "text/javascript">\n'
            header += '\t\tfunction '+word1+word2+' () {\n'
            header += '\n\t\t\tvar element = document.getElementById("'+str(i)+'");\n'
            header += '\t\t\tvar tangle = new Tangle(element, {\n'
            header += '\t\t\t\tinitialize: function() {\n'
            header += '\t\t\t\t\tthis.'+word1+' = 5;\n'
            header += '\t\t\t\t\tthis.'+word2+'Per'+word1+' = '+n_value+';\n'
            header += '\t\t\t\t},\n'
            header += '\t\t\t\tupdate: function () {\n'
            header += '\t\t\t\t\tthis.'+word2+' = this.'+word1+function_value+'this.'+word2+'Per'+word1+';\n'
            header += '\t\t\t\t}\n'
            header += '\t\t\t});\n'
            header += '\t\t}\n'
            header += '\t</script>\n'

        header += '</head>'

        self.header = header

    def do_add_maxmin_count(self):

        match = ''

        for i in range(len(self.count)):
            match = self.cv_list[i*5]

            match = match.lstrip(' ["u')
            match = match.strip("' ")
            match = match.replace(' ','')

            if match == self.count[i][1]:
                self.count[i].append(self.cv_list[1+i*5])
                self.count[i].append(self.cv_list[2+i*5])
            


    def do_body_inject(self):

        final_body = ''
        strip_body = self.txt
        strip_body = self.txt.splitlines()


        n_txt = self.txt.count('\n')

        tangle_functions = ''

        for m in range(len(self.count)):
            tangle_functions += self.count[m][1]+self.count[m][2]+'();'

        final_body = '\n<body onload="'+tangle_functions+'">\n'

        for i in range(n_txt+1):
            working_body = strip_body[i]

            for n in range(len(self.count)):

                search = working_body.find(self.count[n][1])

                if search != -1:

                    search2 = working_body.find(self.count[n][2])


                    final_body += '\t<p id="'+self.count[n][0]+'">\n'
                    final_body += '\t\t'+working_body[:search]+'<span data-var="'+self.count[n][1]+'" class="TKAdjustableNumber" data-min="'+self.count[n][3]+'" data-max="'+self.count[n][4]+'"> '+self.count[n][1]+'</span>'+working_body[search+len(self.count[n][1]):search2]+'<span data-var="'+self.count[n][2]+'"></span> '+working_body[search2:]+'\n'
                    final_body += '\t</p>\n\n'

            if search != -1:
                pass
            else:
                final_body += '\t<p>\n'
                final_body += '\t'+working_body+'\n'
                final_body += '\t</p>\n\n'

        final_body += '</body>\n'
        final_body += '</html>'
        self.body = final_body

    def do_assemble(self):
        compiled = self.header + self.body
        fout = open('coreoutput.html', 'w')
        fout.write(compiled)
        fout.close()
        print compiled

    def main(self):
        core.indexer(self)
        core.do_header_inject(self)
        core.do_add_maxmin_count(self)
        core.do_body_inject(self)
        core.do_assemble(self)

core().main()