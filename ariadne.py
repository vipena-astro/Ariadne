#Code by:       Valentín Peña-Donaire
#Institution:   Instituto de Astrofísica, Facultad de Física, Pontificia Universidad Católica de Chile (The Pontifical Catholic University of Chile)
#Position:      BSc student of Astrophysics (last-year as of 2022)
#Contact info:  vipena@uc.cl
#Last update:   February 6, 2022


#============================================================================================================================================================
#A WARNING
#PyPDF2, the library onto which this code heavily relies, is a powerful tool. With the accurate set of skills, I imagine it could even be used to pursue
#purposes that might infringe local or international laws regarding copyrighted PDF materials; and although I do personally believe in public knowledge,
#I am bound to behave within the law, and I hereby encourage you to do so. The fight towards a fully public and fully accessible network of knowledge is not
#one that we must fight, in my opinion, by means of rebellion and guerrillas but by means of respect, diplomacy and plurality.

#============================================================================================================================================================
#GENERALITIES
#   This script is a very backend-lazy code, so it's thought to be run from Python 3.8.2's Idle. It should run in older versions of Python 3, and it might
#   run in most versions of Python 2 if you just change the syntaxis of some prints here and there. I am currently not proficient in frontend coding, so my
#   GUI skills are but the very basic. If you'd like to implement it, please feel welcome to do so! I would love to know from you if that's the case though,
#   maybe HMU on my email?
#   The lines in this file are optimized for full-screen visualization for font 12, Courier New, bold, within Python 3.8.2's Idle.
#   Uppercase words in comments reference other comments where they are defined.
#   This script receives as an input an original, unindexed PDF file to index, and a user-written TXT index to the PDF file chapters and sections.
#   There is an Appendix at the end of this script that explains the structure the user-written TXT index is to follow.
#   When comments explain the flow of functions, each function is assigned a latin letter (A, B, C...), and the steps within that function are numbered
#   When comments explain the mainflow, only numbers are used (e.g., the second nested flow within the fifth nested flow of the mainflow would be 5.2)
#   Comments with multiple octothorpes (i.e. the hash sign) are addressed to advanced users:
#       A doubled octothorpe means something that can be improved
#       A tripled octothorpe means something that should be improved
#       Octothorpes in groups of four are stuff I was to comment but I forgot. If you find one, please don't hesitate to send me an email! I do check it ;)
#   I use some latinisms across these comments... Sorry! That's a side effect of having studied (therefore extensively reading diverse-centuried textbooks)
#   Astrophysics and [Roman Catholic] Theology. Here's a brief list in case you are lost:
#   Abbreviation    Latinism            Meaning             Usage
#   i.e.            ist ede             that is             "A, i.e. B" means "A, or in other words, B"
#   e.g.            exemplum gratia     example by grace    "[complex concept], e.g. [illustratory example(s)]". Exemplum is singular, exempla is plural, but
#                   exempla gratia                          the abbreviation is the same for both. Fun fact: in Spanish there's a single word for this very
#                                                           same concept: "verbigracia". In old (XIX to early XX cent. books) it was abbreviated "vgr."
#   viz.            videlicet           namely              Similar to "e.g.": "[newly defined general concept] viz. [full list of the things it includes]"
#   cf.             confer              compare             "[explanation full of weird concepts], cf. [external source, or a different part of the text]"

#============================================================================================================================================================
#BASIC CONCEPTS USED IN THE COMMENTS:
#   "HYERARCHICAL STRUCTURE": Text indexation follows, in most scenarios, a HYERARCHICAL STRUCTURE in which SECTIONS are contained in one another in an
#      orderly way, e.g. Chapter 1 may contain Sections 1.1, 1.2, through 1.5; whilst Section 1.4 may contain Subsection 1.4.1, 1.4.2, etc. We humans
#      give different names to different LEVELS in such a HYERARCHICAL STRUCTURE (although the naming probably varies across publishing companies), but
#      in this script philosophy every SECTION is the same kind of object as the others; what changes is "where" it is, i.e. under which upper SECTION it is
#      contained and in which place within that upper LEVEL's subLEVELs is it located.
#   "LEVEL": How deep in the HYERARCHICAL STRUCTURE a specific SECTION is
#   "SECTION": A specific part of the document to be indexed. It may be a Chapter, Section, Subsection, etc.
#   "ROUTE": The full "address" of a SECTION within the HYERARCHICAL STRUCTURE, e.g. for Subsection 3.2.10, its ROUTE would be "SECTION 3 from LEVEL 1,
#      SECTION 2 from LEVEL 2, SECTION 10 from LEVEL 3"

#   "VIRTUAL MAP": An ordered data structure (e.g., a list) that points to a specific ROUTE that the script is working at. It is self-modified as the script
#      goes through the HYERARCHICAL STRUCTURE, indexing its way out into a newly-generated PDF file.



#============================================================================================================================================================
#GLOBALLY-USEFUL FUNCTIONS
def savetitle(data):                                                                    #Get the user-specified title for the working PDF
    title = data.pop(0)[0]
    return title

#============================================================================================================================================================
#BASE VARIABLES AND FUNCTIONS
#   VARIABLES
directory = ''                                                      #Work from the same-level folder TXT index and unindexed PDF files
data_file_name = ''                                                 #Name of the unindexed PDF file as stored in the directory folder
delay = 0                                                           #How shifted is a page in the PDF file numbering system from its content's system
family_tree = [None]                                                #Container for a self-modifying VIRTUAL MAP to the HYERARCHICAL STRUCTURE
                                                                    #   defined in the TXT index. 'None' is a placeholder initialization value,
                                                                    #   meaning the outermost LEVEL in the HYERARCHICAL STRUCTURE, i.e. the whole PDF book
patriarch = None                                                    #Pointer to the SECTION containing those the script is working with at each time.

#   FUNCTIONS
#   A.  Reading the user-provided TXT index
def get_usrindex():
    global data_file_name
    global directory
    data_file_name = input('''Enter the file name (without the ".txt" extension, folders along the path separated by "/") containing the hand-copied index.
Remember both that the original, unindexed PDF file and the TXT index you typeset for it must be within the same folder.
Path to TXT index:\t''')
    location = data_file_name.split('/')
    data_file_name = location.pop(-1)                               #A.1    Identifying the file name as the last part of the user-inputted directory path
    directory = ''                                                  #       The remaining parts are stitched back together as to generate the directory,
    for i in location:                                              #       which just modifies a global variable (cf. above: "Base Variables")
        directory += i + '/'
    
    data_file = open(directory + data_file_name + '.txt', 'rb')     #A.2    Reading the info from the user-provided TXT index and
    data = list(map(lambda s : s.strip().decode().split(' _'), data_file.readlines())) #interpreting it( cf. Appendix I)
    data_file.close()
    return data, data_file_name                                     #A.3    Returning the script-internal version of the HYERARCHICAL STRUCTURE (as 'data')
                                                                    #       and the TXT index file name (as 'data_file_name').


#   B.  Creating the digital index in the working PDF
def do_indexing(new_pdf, data, N):
    global family_tree
    global patriarch
    global delay
    data = np.array(data).T                                         #B.1    Express DATA as 2 columns, data[:,0] contains SECTIONs names and data[:,1]
    for i in range(len(data)):                                      #       contains SECTIONs pages. Then, for each section written in the TXT index,
        print(i, data[i])                                           ##This is a way for the user to watch how the script maps their hand-typeset index onto
                                                                    ##the working PDF. It could be improved by designing a nice front-end GUI to it :)
        if data[i][0]=='!':                                         #B.2    if the shift between page numbering systems is not constant, then the correspon-
            new_delay=data[i][1:][0].split(' ')                     #       dence may be updated by a "!"-flagged line in the TXT file (cf. Appendix I).
            delay = int(new_delay[-1]) - int(new_delay[-2])         #       B.2 reacts to that and updates the global variable DELAY.
            continue
        n = data[i][0]                                              #B.3    Otherwise, read the name of the SECTION and
        points = 0                                                  #       create a placeholder fo the LEVEL of the SECTION. A zero means top-level,
                                                                    #       i.e. the book itself (cf. Appendix I).
        index = data[i][1]                                          #       Also read the page where the SECTION is to be indexed (in the PDF text numbering)
        while '.' in index:                                         #B.4    Counting how many points after the page number, i.e. get the depth of the LEVEL.
            index = index[:-1]
            points += 1
        if points > len(family_tree) - 1:                           #       If we are going down a LEVEL (with respect to the (i-1)-th SECTION), then
            family_tree.append(patriarch)                           #       let the current PATRIARCH into the last point in the ROUTE;
        elif points < len(family_tree) - 1:                         #       whereas if we are going up some LEVELs (with respect to the (i-1)-th SECTION),
            upwards = len(family_tree) - points - 1                 #       count how many LEVELs are we rising and
            for i in range(upwards):
                family_tree.pop(-1)                                 #       go back Ariadne's thread through the ROUTE, popping the LEVELs we climb.                
        p = int(index) - 1 + delay                                  #B.5    Compute the final index where the SECTION will be marked in the working PDF
        patriarch=new_pdf.addBookmark(n,p,parent=family_tree[-1])   #B.6    This does the actual indexation into the working PDF.
    return new_pdf                                                  #B.7    Return the newly-indexed PDF



#   C.  Managing PDF file creation and destruction
def manage_pdffiles(data):
    inp_file = open(directory + title + '.pdf', 'rb')                   #C.1    Open the input PDF file and create the corresponding PyPDF2 object
    inp_pdf = pdf.PdfFileReader(inp_file)

    new_pdf = pdf.PdfFileWriter()                                       #C.2    Create a blank PDF file (hereforth the "working" PDF) with PyPDF2 and
    N = inp_pdf.numPages                                                #       determine the number of pages of the original PDF file.
    for i in range(N):                                                  #C.3    Programatically copy the content from the original PDF to the working one
        new_pdf.addPage(inp_pdf.getPage(i))

    new_pdf = do_indexing(new_pdf, data, N)                             #C.4    Index each SECTION onto the working PDF as indicated in the TXT file
    with open(directory + title + '_indexed.pdf', 'wb') as out_file:    #C.5    Save the newly-indexed PDF
        new_pdf.write(out_file)
        
    inp_file.close()
    out_file.close()
    print('Success! <3')
    return



#============================================================================================================================================================
#MAINLOOP
if __name__ == "__main__":
    import numpy as np
    import PyPDF2 as pdf                                            #This is the main library used to read/write PDF pages. It allows for indexation.

    
    trash = []                                                      ##Container for stuff I dumped, just in case you need it

    data, data_file_name = get_usrindex()                           #1.     Read the user-provided TXT index into a script-internal HYERARCHICAL STRUCTURE
    #print(data)                                                    ##Devise a nice-looking, user-friendly way to print the HYERARCHICAL STRUCTURE on screen
                                                                    ##so that the user can know their TXT index has been properly read
    title = savetitle(data)                                         #1.1    Store the user-defined title of the new PDF to generate. It should be defined in
                                                                    #       the first line of the TXT index, cf. Appendix I below.

    line = data.pop(0)                                              #2.     Determining the delay between the PDF file page numbering and its text page
    delay_info = line[0].split(' ')                                 #       numbering, cf. Appendix I. This is usual in digital books. 
    trash.append(data.pop(0))
    try:
        delay = int(delay_info[-1]) - int(delay_info[-2])
        data[0] = data[0][:2]                                       #2.1    Strip DATA from the first two lines of the TXT index, viz. the delay info and a
        data = list(np.array(data).T)                               #       blank line. What follows is transposed as a np.ndarray to generate columned info
    except ValueError:                                              #2.2    If no delay is specified, hence what follows the TITLE in the TXT file is just a
        delay = 0                                                   #       blank line, the script assumes there's no delay (e.g., for scanned class notes).
    print('delay = ', delay)
    data = np.array(data)                                           #2.3    Store data in a numpy.ndarray

    manage_pdffiles(data)                                           #3.     Create a copy of the original PDF onto which to index each SECTION.

#============================================================================================================================================================
#BIBLIOGRAPHY
#Beyond Python itself, this script uses two libraries not coded by me:
#   library     version     reference                   credit    
#   NumPy       1.22.0      numpy.org                   Harris, C.R., Millman, K.J., van der Walt, S.J. et al. Array programming with NumPy.
#                                                          Nature 585, 357-362 (2020). DOI: 10.1038/s41586-020-2649-2
#   PyPDF2      1.26.0      github.com/mstamy/PyPDF2    Matthew Stamy, 2018

#============================================================================================================================================================
#Appendix I: THE USER-PROVIDED TXT INDEX FILE
    
#As stated in the preamble, this script feeds of a TXT file containing an index manually typeset by you prior to running this indexing algorithm.
#In this Appendix, I intend to explain the general structure of such a manual index.

#Part   #Line(s)        #Data and format
# 1     1               The title of the new, digitally indexed PDF file to create. This is how it will be saved to your system, so remember to not use
#                       forbidden characters
#
#       2               Two positive integers, separated by a simple space. This represents the shift between the digital (in-file) and visual (on-page) page
#                       numbering systems. Put simply, if you were to index page 30 of your novel onto page 34 of the PDF (e.g., if you want to intentionally
#                       leave 4 unnumbered pages at the beginning), in this line you'd have to write "30 34" (without the quotation marks)
#
#       3               A blank line (DO NOT FORGET TO LEAVE A BLANK LINE HERE!!!)
#
# 2     everything      Now you write down the proper index. On each line, write the full name to a SECTION, then one simple space, then a single underscore,
#                       then the page number where you want it indexed in the visual (on-page) system. Immediately after the number, you'll have to write
#                       down a series of dots, as many as deep the LEVEL of the SECTION in this line is within the HYERARCHICAL STRUCTURE (cf. the general
#                       concepts up in the preamble for an explanation). You can also check the example provided alongside this code to get a feeling of how
#                       the dot-coding of depth works.
# 2     incidental      IF you wanted to skip numbers in the on-page system (e.g., you don't want to have a 4-th page but instead jump straight from page 3
#                       to page 5 for religious reasons; or if you were to index the (PROPERLY AUTHORISED) scanning of a book where some pages went missing),
#                       you might think "Oh but wait, I will have problems with the delay between page numbering systems"... Well, fear not, for you can
#                       update the shift between systems mid-index. Simply write a line in the format "! _A B" (without the quotation marks), where A and B
#                       are positive integers defined in the same way as in the second line of your TXT file.



#============================================================================================================================================================
#I've said it in the preamble and I want to remark it again: if you are having trouble learning to use thi  code or get more stuck than it'd be healthy to
#endure, please do email me with your inquiries and I'll be glad to help you. I might take a couple weeks just in case I'm extra busy, but I do read all my
#emails. My address is vipena@uc.cl

#Love from latitude 33 South!
