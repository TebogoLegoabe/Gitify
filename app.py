from flask import Flask, render_template, request, redirect, url_for, abort
from utils import get_languages_lite as get_language
import requests
from os import getenv
import datetime

REPOS_PER_PAGE = 5
USERS_PER_PAGE = 4

access_token = getenv("ACCESS_TOKEN")

headers = {
    'Authorization': f'token {access_token}',
    'Accept': 'application/vnd.github.v3+json',
}
options = {
    "sort_by" : [
             ("_desc", "Best match"),
             ("stars_desc","Most stars"),
             ("stars_asc","Fewest stars"),
             ("forks_desc","Most Forks"),
             ("forks_asc"," Fewest Forks"),
             ("updated_desc", "Recently updated"),
             ("updated_asc", "Least recently updated"),
    ],
    "colors" : {
        "Python": "#3776AB", # Blue
        "Java": "#B07219", # Brown
        "JavaScript": "#F7DF1E", # Yellow
        "C#": "#178600", # Green
        "C++": "#00599C", # Dark blue
        "PHP": "#777BB4", # Purple
        "R": "#198CE7", # Light blue
        "TypeScript": "#3178C6", # Cyan
        "Swift": "#FA7343", # Orange
        "C": "#438EFF", # Sky blue
        "Kotlin": "#F18E33", # Amber
        "Makefile": "#427B58", # Olive green
        "Others": "#666666" # gray 
    },
    "popular_lang" : [ ("C","C"),("C#","C#"), ("C++","C++"), ("CoffeeScript","CoffeeScript"),("CSS","CSS"), ("Dart","Dart"),("DM","DM"), ("Elixir","Elixir"), ("Go","Go"),("Groovy","Groovy"), ("HTML","HTML"), ("Java","Java"), ("JavaScript","JavaScript"), ("Kotlin","Kotlin"), ("Objective-C","Objective-C"), ("Perl","Perl"), ("PHP","PHP"), ("PowerShell","PowerShell"), ("Python","Python"), ("Ruby","Ruby"), ("Rust","Rust"), ("Scala","Scala"), ("Shell","Shell"), ("Swift","Swift"), ("TypeScript","TypeScript")],
    "everything_lang" : [("1C Enterprise","1C Enterprise"), ("2-Dimensional Array","2-Dimensional Array"), ("4D","4D"), ("ABAP","ABAP"), ("ABAP CDS","ABAP CDS"), ("ABNF","ABNF"), ("ActionScript","ActionScript"), ("Ada","Ada"), ("Adblock Filter List","Adblock Filter List"), ("Adobe Font Metrics","Adobe Font Metrics"), ("Agda","Agda"), ("AGS Script","AGS Script"), ("AIDL","AIDL"), ("AL","AL"), ("Alloy","Alloy"), ("Alpine Abuild","Alpine Abuild"), ("Altium Designer","Altium Designer"), ("AMPL","AMPL"), ("AngelScript","AngelScript"), ("Ant Build System","Ant Build System"), ("Antlers","Antlers"), ("ANTLR","ANTLR"), ("ApacheConf","ApacheConf"), ("Apex","Apex"), ("API Blueprint","API Blueprint"), ("APL","APL"), ("Apollo Guidance Computer","Apollo Guidance Computer"), ("AppleScript","AppleScript"), ("Arc","Arc"), ("AsciiDoc","AsciiDoc"), ("ASL","ASL"), ("ASN.1","ASN.1"), ("ASP.NET","ASP.NET"), ("AspectJ","AspectJ"), ("Assembly","Assembly"), ("Astro","Astro"), ("Asymptote","Asymptote"), ("ATS","ATS"), ("Augeas","Augeas"), ("AutoHotkey","AutoHotkey"), ("AutoIt","AutoIt"), ("Avro IDL","Avro IDL"), ("Awk","Awk"), ("Ballerina","Ballerina"), ("BASIC","BASIC"), ("Batchfile","Batchfile"), ("Beef","Beef"), ("Befunge","Befunge"), ("Berry","Berry"), ("BibTeX","BibTeX"), ("Bicep","Bicep"), ("Bikeshed","Bikeshed"), ("Bison","Bison"), ("BitBake","BitBake"), ("Blade","Blade"), ("BlitzBasic","BlitzBasic"), ("BlitzMax","BlitzMax"), ("Bluespec","Bluespec"), ("Bluespec BH","Bluespec BH"), ("Boo","Boo"), ("Boogie","Boogie"), ("Brainfuck","Brainfuck"), ("BrighterScript","BrighterScript"), ("Brightscript","Brightscript"), ("Browserslist","Browserslist"), ("C-ObjDump","C-ObjDump"), ("C2hs Haskell","C2hs Haskell"), ("Cabal Config","Cabal Config"), ("Cadence","Cadence"), ("Cairo","Cairo"), ("CameLIGO","CameLIGO"), ("CAP CDS","CAP CDS"), ("Cap'n Proto","Cap'n Proto"), ("CartoCSS","CartoCSS"), ("Ceylon","Ceylon"), ("Chapel","Chapel"), ("Charity","Charity"), ("Checksums","Checksums"), ("ChucK","ChucK"), ("CIL","CIL"), ("Circom","Circom"), ("Cirru","Cirru"), ("Clarion","Clarion"), ("Clarity","Clarity"), ("Classic ASP","Classic ASP"), ("Clean","Clean"), ("Click","Click"), ("CLIPS","CLIPS"), ("Clojure","Clojure"), ("Closure Templates","Closure Templates"), ("Cloud Firestore Security Rules","Cloud Firestore Security Rules"), ("CMake","CMake"), ("COBOL","COBOL"), ("CODEOWNERS","CODEOWNERS"), ("CodeQL","CodeQL"), ("ColdFusion","ColdFusion"), ("ColdFusion CFC","ColdFusion CFC"), ("COLLADA","COLLADA"), ("Common Lisp","Common Lisp"), ("Common Workflow Language","Common Workflow Language"), ("Component Pascal","Component Pascal"), ("CoNLL-U","CoNLL-U"), ("Cool","Cool"), ("Coq","Coq"), ("Cpp-ObjDump","Cpp-ObjDump"), ("Creole","Creole"), ("Crystal","Crystal"), ("CSON","CSON"), ("Csound","Csound"), ("Csound Document","Csound Document"), ("Csound Score","Csound Score"), ("CSV","CSV"), ("Cuda","Cuda"), ("CUE","CUE"), ("Cue Sheet","Cue Sheet"), ("cURL Config","cURL Config"), ("Curry","Curry"), ("CWeb","CWeb"), ("Cycript","Cycript"), ("Cypher","Cypher"), ("Cython","Cython"), ("D","D"), ("D-ObjDump","D-ObjDump"), ("D2","D2"), ("Dafny","Dafny"), ("Darcs Patch","Darcs Patch"), ("DataWeave","DataWeave"), ("Debian Package Control File","Debian Package Control File"), ("DenizenScript","DenizenScript"), ("desktop","desktop"), ("Dhall","Dhall"), ("Diff","Diff"), ("DIGITAL Command Language","DIGITAL Command Language"), ("dircolors","dircolors"), ("DirectX 3D File","DirectX 3D File"), ("DNS Zone","DNS Zone"), ("Dockerfile","Dockerfile"), ("Dogescript","Dogescript"), ("Dotenv","Dotenv"), ("DTrace","DTrace"), ("Dylan","Dylan"), ("E","E"), ("E-mail","E-mail"), ("Eagle","Eagle"), ("Earthly","Earthly"), ("Easybuild","Easybuild"), ("EBNF","EBNF"), ("eC","eC"), ("Ecere Projects","Ecere Projects"), ("ECL","ECL"), ("ECLiPSe","ECLiPSe"), ("Ecmarkup","Ecmarkup"), ("EditorConfig","EditorConfig"), ("Edje Data Collection","Edje Data Collection"), ("edn","edn"), ("Eiffel","Eiffel"), ("EJS","EJS"), ("Elm","Elm"), ("Elvish","Elvish"), ("Elvish Transcript","Elvish Transcript"), ("Emacs Lisp","Emacs Lisp"), ("EmberScript","EmberScript"), ("EQ","EQ"), ("Erlang","Erlang"), ("Euphoria","Euphoria"), ("F#","F#"), ("F*","F*"), ("Factor","Factor"), ("Fancy","Fancy"), ("Fantom","Fantom"), ("Faust","Faust"), ("Fennel","Fennel"), ("FIGlet Font","FIGlet Font"), ("Filebench WML","Filebench WML"), ("Filterscript","Filterscript"), ("fish","fish"), ("Fluent","Fluent"), ("FLUX","FLUX"), ("Formatted","Formatted"), ("Forth","Forth"), ("Fortran","Fortran"), ("Fortran Free Form","Fortran Free Form"), ("FreeBasic","FreeBasic"), ("FreeMarker","FreeMarker"), ("Frege","Frege"), ("Futhark","Futhark"), ("G-code","G-code"), ("Game Maker Language","Game Maker Language"), ("GAML","GAML"), ("GAMS","GAMS"), ("GAP","GAP"), ("GCC Machine Description","GCC Machine Description"), ("GDB","GDB"), ("GDScript","GDScript"), ("GEDCOM","GEDCOM"), ("Gemfile.lock","Gemfile.lock"), ("Gemini","Gemini"), ("Genero","Genero"), ("Genero Forms","Genero Forms"), ("Genie","Genie"), ("Genshi","Genshi"), ("Gentoo Ebuild","Gentoo Ebuild"), ("Gentoo Eclass","Gentoo Eclass"), ("Gerber Image","Gerber Image"), ("Gettext Catalog","Gettext Catalog"), ("Gherkin","Gherkin"), ("Git Attributes","Git Attributes"), ("Git Config","Git Config"), ("Git Revision List","Git Revision List"), ("Gleam","Gleam"), ("GLSL","GLSL"), ("Glyph","Glyph"), ("Glyph Bitmap Distribution Format","Glyph Bitmap Distribution Format"), ("GN","GN"), ("Gnuplot","Gnuplot"), ("Go Checksums","Go Checksums"), ("Go Module","Go Module"), ("Go Workspace","Go Workspace"), ("Godot Resource","Godot Resource"), ("Golo","Golo"), ("Gosu","Gosu"), ("Grace","Grace"), ("Gradle","Gradle"), ("Gradle Kotlin DSL","Gradle Kotlin DSL"), ("Grammatical Framework","Grammatical Framework"), ("Graph Modeling Language","Graph Modeling Language"), ("GraphQL","GraphQL"), ("Graphviz (DOT)","Graphviz (DOT)"), ("Groovy Server Pages","Groovy Server Pages"), ("GSC","GSC"), ("Hack","Hack"), ("Haml","Haml"), ("Handlebars","Handlebars"), ("HAProxy","HAProxy"), ("Harbour","Harbour"), ("Haskell","Haskell"), ("Haxe","Haxe"), ("HCL","HCL"), ("HiveQL","HiveQL"), ("HLSL","HLSL"), ("HOCON","HOCON"), ("HolyC","HolyC"), ("hoon","hoon"), ("Hosts File","Hosts File"), ("HTML+ECR","HTML+ECR"), ("HTML+EEX","HTML+EEX"), ("HTML+ERB","HTML+ERB"), ("HTML+PHP","HTML+PHP"), ("HTML+Razor","HTML+Razor"), ("HTTP","HTTP"), ("HXML","HXML"), ("Hy","Hy"), ("HyPhy","HyPhy"), ("IDL","IDL"), ("Idris","Idris"), ("Ignore List","Ignore List"), ("IGOR Pro","IGOR Pro"), ("ImageJ Macro","ImageJ Macro"), ("Imba","Imba"), ("Inform 7","Inform 7"), ("INI","INI"), ("Ink","Ink"), ("Inno Setup","Inno Setup"), ("Io","Io"), ("Ioke","Ioke"), ("IRC log","IRC log"), ("Isabelle","Isabelle"), ("Isabelle ROOT","Isabelle ROOT"), ("J","J"), ("Janet","Janet"), ("JAR Manifest","JAR Manifest"), ("Jasmin","Jasmin"), ("Java Properties","Java Properties"), ("Java Server Pages","Java Server Pages"), ("JavaScript+ERB","JavaScript+ERB"), ("JCL","JCL"), ("Jest Snapshot","Jest Snapshot"), ("JetBrains MPS","JetBrains MPS"), ("JFlex","JFlex"), ("Jinja","Jinja"), ("Jison","Jison"), ("Jison Lex","Jison Lex"), ("Jolie","Jolie"), ("jq","jq"), ("JSON","JSON"), ("JSON with Comments","JSON with Comments"), ("JSON5","JSON5"), ("JSONiq","JSONiq"), ("JSONLD","JSONLD"), ("Jsonnet","Jsonnet"), ("Julia","Julia"), ("Jupyter Notebook","Jupyter Notebook"), ("Just","Just"), ("Kaitai Struct","Kaitai Struct"), ("KakouneScript","KakouneScript"), ("KerboScript","KerboScript"), ("KiCad Layout","KiCad Layout"), ("KiCad Legacy Layout","KiCad Legacy Layout"), ("KiCad Schematic","KiCad Schematic"), ("Kickstart","Kickstart"), ("Kit","Kit"), ("KRL","KRL"), ("Kusto","Kusto"), ("kvlang","kvlang"), ("LabVIEW","LabVIEW"), ("Lark","Lark"), ("Lasso","Lasso"), ("Latte","Latte"), ("Lean","Lean"), ("Less","Less"), ("Lex","Lex"), ("LFE","LFE"), ("LigoLANG","LigoLANG"), ("LilyPond","LilyPond"), ("Limbo","Limbo"), ("Linker Script","Linker Script"), ("Linux Kernel Module","Linux Kernel Module"), ("Liquid","Liquid"), ("Literate Agda","Literate Agda"), ("Literate CoffeeScript","Literate CoffeeScript"), ("Literate Haskell","Literate Haskell"), ("LiveScript","LiveScript"), ("LLVM","LLVM"), ("Logos","Logos"), ("Logtalk","Logtalk"), ("LOLCODE","LOLCODE"), ("LookML","LookML"), ("LoomScript","LoomScript"), ("LSL","LSL"), ("LTspice Symbol","LTspice Symbol"), ("Lua","Lua"), ("M","M"), ("M4","M4"), ("M4Sugar","M4Sugar"), ("Macaulay2","Macaulay2"), ("Makefile","Makefile"), ("Mako","Mako"), ("Markdown","Markdown"), ("Marko","Marko"), ("Mask","Mask"), ("Mathematica","Mathematica"), ("MATLAB","MATLAB"), ("Maven POM","Maven POM"), ("Max","Max"), ("MAXScript","MAXScript"), ("mcfunction","mcfunction"), ("MDX","MDX"), ("Mercury","Mercury"), ("Mermaid","Mermaid"), ("Meson","Meson"), ("Metal","Metal"), ("Microsoft Developer Studio Project","Microsoft Developer Studio Project"), ("Microsoft Visual Studio Solution","Microsoft Visual Studio Solution"), ("MiniD","MiniD"), ("MiniYAML","MiniYAML"), ("Mint","Mint"), ("Mirah","Mirah"), ("mIRC Script","mIRC Script"), ("MLIR","MLIR"), ("Modelica","Modelica"), ("Modula-2","Modula-2"), ("Modula-3","Modula-3"), ("Module Management System","Module Management System"), ("Monkey","Monkey"), ("Monkey C","Monkey C"), ("Moocode","Moocode"), ("MoonScript","MoonScript"), ("Motoko","Motoko"), ("Motorola 68K Assembly","Motorola 68K Assembly"), ("Move","Move"), ("MQL4","MQL4"), ("MQL5","MQL5"), ("MTML","MTML"), ("MUF","MUF"), ("mupad","mupad"), ("Muse","Muse"), ("Mustache","Mustache"), ("Myghty","Myghty"), ("nanorc","nanorc"), ("Nasal","Nasal"), ("NASL","NASL"), ("NCL","NCL"), ("Nearley","Nearley"), ("Nemerle","Nemerle"), ("NEON","NEON"), ("nesC","nesC"), ("NetLinx","NetLinx"), ("NetLinx+ERB","NetLinx+ERB"), ("NetLogo","NetLogo"), ("NewLisp","NewLisp"), ("Nextflow","Nextflow"), ("Nginx","Nginx"), ("Nim","Nim"), ("Ninja","Ninja"), ("Nit","Nit"), ("Nix","Nix"), ("NL","NL"), ("NPM Config","NPM Config"), ("NSIS","NSIS"), ("Nu","Nu"), ("NumPy","NumPy"), ("Nunjucks","Nunjucks"), ("Nushell","Nushell"), ("NWScript","NWScript"), ("OASv2-json","OASv2-json"), ("OASv2-yaml","OASv2-yaml"), ("OASv3-json","OASv3-json"), ("OASv3-yaml","OASv3-yaml"), ("ObjDump","ObjDump"), ("Object Data Instance Notation","Object Data Instance Notation"), ("Objective-C++","Objective-C++"), ("Objective-J","Objective-J"), ("ObjectScript","ObjectScript"), ("OCaml","OCaml"), ("Odin","Odin"), ("Omgrofl","Omgrofl"), ("ooc","ooc"), ("Opa","Opa"), ("Opal","Opal"), ("Open Policy Agent","Open Policy Agent"), ("OpenAPI Specification v2","OpenAPI Specification v2"), ("OpenAPI Specification v3","OpenAPI Specification v3"), ("OpenCL","OpenCL"), ("OpenEdge ABL","OpenEdge ABL"), ("OpenQASM","OpenQASM"), ("OpenRC runscript","OpenRC runscript"), ("OpenSCAD","OpenSCAD"), ("OpenStep Property List","OpenStep Property List"), ("OpenType Feature File","OpenType Feature File"), ("Option List","Option List"), ("Org","Org"), ("Ox","Ox"), ("Oxygene","Oxygene"), ("Oz","Oz"), ("P4","P4"), ("Pact","Pact"), ("Pan","Pan"), ("Papyrus","Papyrus"), ("Parrot","Parrot"), ("Parrot Assembly","Parrot Assembly"), ("Parrot Internal Representation","Parrot Internal Representation"), ("Pascal","Pascal"), ("Pawn","Pawn"), ("PDDL","PDDL"), ("PEG.js","PEG.js"), ("Pep8","Pep8"), ("Pic","Pic"), ("Pickle","Pickle"), ("PicoLisp","PicoLisp"), ("PigLatin","PigLatin"), ("Pike","Pike"), ("PlantUML","PlantUML"), ("PLpgSQL","PLpgSQL"), ("PLSQL","PLSQL"), ("Pod","Pod"), ("Pod 6","Pod 6"), ("PogoScript","PogoScript"), ("Polar","Polar"), ("Pony","Pony"), ("Portugol","Portugol"), ("PostCSS","PostCSS"), ("PostScript","PostScript"), ("POV-Ray SDL","POV-Ray SDL"), ("PowerBuilder","PowerBuilder"), ("Prisma","Prisma"), ("Processing","Processing"), ("Procfile","Procfile"), ("Proguard","Proguard"), ("Prolog","Prolog"), ("Promela","Promela"), ("Propeller Spin","Propeller Spin"), ("Protocol Buffer","Protocol Buffer"), ("Protocol Buffer Text Format","Protocol Buffer Text Format"), ("Public Key","Public Key"), ("Pug","Pug"), ("Puppet","Puppet"), ("Pure Data","Pure Data"), ("PureBasic","PureBasic"), ("PureScript","PureScript"), ("Pyret","Pyret"), ("Python console","Python console"), ("Python traceback","Python traceback"), ("q","q"), ("Q#","Q#"), ("QMake","QMake"), ("QML","QML"), ("Qt Script","Qt Script"), ("Quake","Quake"), ("R","R"), ("Racket","Racket"), ("Ragel","Ragel"), ("Raku","Raku"), ("RAML","RAML"), ("Rascal","Rascal"), ("Raw token data","Raw token data"), ("RBS","RBS"), ("RDoc","RDoc"), ("Readline Config","Readline Config"), ("REALbasic","REALbasic"), ("Reason","Reason"), ("ReasonLIGO","ReasonLIGO"), ("Rebol","Rebol"), ("Record Jar","Record Jar"), ("Red","Red"), ("Redcode","Redcode"), ("Redirect Rules","Redirect Rules"), ("Regular Expression","Regular Expression"), ("Ren'Py","Ren'Py"), ("RenderScript","RenderScript"), ("ReScript","ReScript"), ("reStructuredText","reStructuredText"), ("REXX","REXX"), ("Rez","Rez"), ("Rich Text Format","Rich Text Format"), ("Ring","Ring"), ("Riot","Riot"), ("RMarkdown","RMarkdown"), ("RobotFramework","RobotFramework"), ("robots.txt","robots.txt"), ("Roff","Roff"), ("Roff Manpage","Roff Manpage"), ("Rouge","Rouge"), ("RouterOS Script","RouterOS Script"), ("RPC","RPC"), ("RPGLE","RPGLE"), ("RPM Spec","RPM Spec"), ("RUNOFF","RUNOFF"), ("Sage","Sage"), ("SaltStack","SaltStack"), ("SAS","SAS"), ("Sass","Sass"), ("Scaml","Scaml"), ("Scenic","Scenic"), ("Scheme","Scheme"), ("Scilab","Scilab"), ("SCSS","SCSS"), ("sed","sed"), ("Self","Self"), ("SELinux Policy","SELinux Policy"), ("ShaderLab","ShaderLab"), ("ShellCheck Config","ShellCheck Config"), ("ShellSession","ShellSession"), ("Shen","Shen"), ("Sieve","Sieve"), ("Simple File Verification","Simple File Verification"), ("Singularity","Singularity"), ("Slash","Slash"), ("Slice","Slice"), ("Slim","Slim"), ("Smali","Smali"), ("Smalltalk","Smalltalk"), ("Smarty","Smarty"), ("Smithy","Smithy"), ("SmPL","SmPL"), ("SMT","SMT"), ("Snakemake","Snakemake"), ("Solidity","Solidity"), ("Soong","Soong"), ("SourcePawn","SourcePawn"), ("SPARQL","SPARQL"), ("Spline Font Database","Spline Font Database"), ("SQF","SQF"), ("SQL","SQL"), ("SQLPL","SQLPL"), ("Squirrel","Squirrel"), ("SRecode Template","SRecode Template"), ("SSH Config","SSH Config"), ("Stan","Stan"), ("Standard ML","Standard ML"), ("STAR","STAR"), ("Starlark","Starlark"), ("Stata","Stata"), ("STL","STL"), ("STON","STON"), ("StringTemplate","StringTemplate"), ("Stylus","Stylus"), ("SubRip Text","SubRip Text"), ("SugarSS","SugarSS"), ("SuperCollider","SuperCollider"), ("Svelte","Svelte"), ("SVG","SVG"), ("Sway","Sway"), ("Sweave","Sweave"), ("SWIG","SWIG"), ("SystemVerilog","SystemVerilog"), ("Talon","Talon"), ("Tcl","Tcl"), ("Tcsh","Tcsh"), ("Tea","Tea"), ("Terra","Terra"), ("TeX","TeX"), ("Texinfo","Texinfo"), ("Text","Text"), ("Textile","Textile"), ("TextMate Properties","TextMate Properties"), ("Thrift","Thrift"), ("TI Program","TI Program"), ("TL-Verilog","TL-Verilog"), ("TLA","TLA"), ("TOML","TOML"), ("TSQL","TSQL"), ("TSV","TSV"), ("TSX","TSX"), ("Turing","Turing"), ("Turtle","Turtle"), ("Twig","Twig"), ("TXL","TXL"), ("Type Language","Type Language"), ("Typst","Typst"), ("Unified Parallel C","Unified Parallel C"), ("Unity3D Asset","Unity3D Asset"), ("Unix Assembly","Unix Assembly"), ("Uno","Uno"), ("UnrealScript","UnrealScript"), ("UrWeb","UrWeb"), ("V","V"), ("Vala","Vala"), ("Valve Data Format","Valve Data Format"), ("VBA","VBA"), ("VBScript","VBScript"), ("VCL","VCL"), ("Velocity Template Language","Velocity Template Language"), ("Verilog","Verilog"), ("VHDL","VHDL"), ("Vim Help File","Vim Help File"), ("Vim Script","Vim Script"), ("Vim Snippet","Vim Snippet"), ("Visual Basic .NET","Visual Basic .NET"), ("Visual Basic 6.0","Visual Basic 6.0"), ("Volt","Volt"), ("Vue","Vue"), ("Vyper","Vyper"), ("Wavefront Material","Wavefront Material"), ("Wavefront Object","Wavefront Object"), ("WDL","WDL"), ("Web Ontology Language","Web Ontology Language"), ("WebAssembly","WebAssembly"), ("WebAssembly Interface Type","WebAssembly Interface Type"), ("WebIDL","WebIDL"), ("WebVTT","WebVTT"), ("Wget Config","Wget Config"), ("WGSL","WGSL"), ("Whiley","Whiley"), ("Wikitext","Wikitext"), ("Win32 Message File","Win32 Message File"), ("Windows Registry Entries","Windows Registry Entries"), ("wisp","wisp"), ("Witcher Script","Witcher Script"), ("Wollok","Wollok"), ("World of Warcraft Addon Data","World of Warcraft Addon Data"), ("Wren","Wren"), ("X BitMap","X BitMap"), ("X Font Directory Index","X Font Directory Index"), ("X PixMap","X PixMap"), ("X10","X10"), ("xBase","xBase"), ("XC","XC"), ("XCompose","XCompose"), ("XML","XML"), ("XML Property List","XML Property List"), ("Xojo","Xojo"), ("Xonsh","Xonsh"), ("XPages","XPages"), ("XProc","XProc"), ("XQuery","XQuery"), ("XS","XS"), ("XSLT","XSLT"), ("Xtend","Xtend"), ("Yacc","Yacc"), ("YAML","YAML"), ("YANG","YANG"), ("YARA","YARA"), ("YASnippet","YASnippet"), ("Yul","Yul"), ("ZAP","ZAP"), ("Zeek","Zeek"), ("ZenScript","ZenScript"), ("Zephir","Zephir"), ("Zig","Zig"), ("ZIL","ZIL"), ("Zimpl","Zimpl")]
    }

app = Flask(__name__)
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(422)
def unprocessable_entity(e):
    return render_template("422.html"), 422

@app.route("/search")
def search_redirect():
  # Get the option parameter from the GET request
    search_for = request.args.get("search_for")
    q = request.args.get("q")
    language = request.args.get("language", "")
    location = request.args.get('location', "")
    sort_by = request.args.get('sort_by', "")
    # Redirect to the corresponding route based on the option value
    if search_for == "repos":
        return redirect(url_for("search_repos",search_for = search_for, q = q, language = language, location = location, sort_by = sort_by))
    elif search_for == "users":
        return redirect(url_for("search_users",search_for = search_for, q = q, language = language, location = location, sort_by = sort_by))
  
@app.route("/")
def home():
    """ home page used for searching"""
    return render_template("search.html")



@app.route('/users', methods=['GET'])
def search_users():
    """ searchs for users in github using github api """
    username = request.args.get("q")
    lang = request.args.get("language", "")
    loc = request.args.get('location', "")
    sort_by = request.args.get('sort_by', "").split('_') if request.args.get('sort_by') else ['','']

    # paramaters used by gitify
    params_g = {
        'q': username,
        "sort_by": sort_by,
        "location": loc,
        "language": lang,
        "per_page": USERS_PER_PAGE,
        "page": int(request.args.get('page', 1))
    }
    if not username:
        return render_template('user_results.html', users=[], options=options, results=-1, p=params_g, language=lang, q=username)
    # parameters used in github api
    params = {
        'q': f'{username} location:"{loc}" language:"{lang}"',
        "sort": sort_by[0],
        "order": sort_by[1],
        "per_page": USERS_PER_PAGE,
        "page": int(request.args.get('page', 1))
    }
    # search for the user
    req = requests.get(f"https://api.github.com/search/users", params=params, headers=headers)
    if req.status_code == 200:
        all_users = req.json()
        # print(all_users)
        users = []
        results_count = all_users['total_count']

        # loops over all users and retrive necessary information about the user
        for user in all_users['items']:
            temp =  {
                "username": user['login'],
                "avatar": user['avatar_url'],
                "html_url": user['html_url']
            }
            # DEBUGGING
            # print("fetching for: ", user['login'])
            # inside a user result you will find 'url' that contains detailed information about the user, and store the info in users_info variable. e.g: https://api.github.com/repos/creytiv/re
            user_info = requests.get(user['url'], headers=headers).json()
            
            # fetching user's information
            temp['followers'] = user_info['followers']
            temp['following'] = user_info['following']
            temp['bio'] = user_info['bio']
            temp['location'] = user_info.get('location', 'Unknown')
            # inside the user_info the 'public_repos' key holds the number of public repositories the user owns
            temp['public_repos'] = user_info['public_repos']
            # inside the 'repos_url the 'repos_url' key holds a link to all the repositories the user owns. e.g : https://api.github.com/users/Qihoo360
            # what the get_language function does is: it accepts a repos_url, adds all the language usages of that user in each repository, calculates their usage percentage,returns a dictionary of languages, when you use the .itmes() the result will be as follows. eg: [('Java', 21.43), ('Kotlin', 21.43), ('Python', 14.29), ('Others', 42.85)]
            unfiltered_lang = get_language(user_info['repos_url']).items()

            # the code bellow is a filtering mechanism: it selects top 3 languages used, sum the other languages and adds them as a forth language
            sorted_lang = sorted(unfiltered_lang,key=lambda ln: ln[1], reverse=True)
            temp['languages'] = sorted_lang[0:3]
            remained = 0
            for t in temp['languages']:
                remained += t[1]
            temp['languages'].append(('Others', 100 - remained))
            # adds the user's info to the list of users
            users.append(temp)

        # print(users)
        return render_template('user_results.html', users=users, options=options, results=results_count, p=params_g, language=lang,q=username)
    else:
        return f"Error: status code - {req.status_code}"



 
@app.route('/repos', methods=['GET'])
def search_repos():
    """ search repos by the given key word """

    q = request.args.get("q")
    sort_by = request.args.get('sort_by').split('_') if request.args.get('sort_by') else ['','']
    lang = request.args.get("language", "")
    params_g = {
        'q': q,
        "sort_by": request.args.get('sort_by', ""),
        "language": lang,
        "per_page": REPOS_PER_PAGE,
        "page": int(request.args.get('page', 1))
    }
    if not q:
        return render_template('repo_results.html', results=-1, page=0, options=options, p=params_g)

    params = {
        'q': f'{q} language:"{lang}"' if lang else q,
        "sort": sort_by[0],
        "order": sort_by[1],
        "per_page": REPOS_PER_PAGE,
        "page": int(request.args.get('page', 1))
    }
    colors = {
            "Python": "#3776AB", # Blue
            "Java": "#B07219", # Brown
            "JavaScript": "#F7DF1E", # Yellow
            "C#": "#178600", # Green
            "C++": "#00599C", # Dark blue
            "PHP": "#777BB4", # Purple
            "R": "#198CE7", # Light blue
            "TypeScript": "#3178C6", # Cyan
            "Swift": "#FA7343", # Orange
            "C": "#438EFF", # Sky blue
            "Kotlin": "#F18E33", # Amber
            "Makefile": "#427B58", # Olive green
            "Others": "#666666" # gray 
    }

    response = requests.get("https://api.github.com/search/repositories", params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        items = data["items"]
        results_count = data['total_count']

        repos = []
        # print(f"Found {len(items)} trending repositories:")
        for item in items:
            temp = {}
            temp['name'] = item['name']
            temp['description'] = item['description']
            temp['html_url'] = item['html_url']
            temp['owner'] = item['owner']['login']
            temp['avatar'] = item['owner']['avatar_url']
            temp['language'] = item['language']
            temp['stars'] = item['stargazers_count']
            temp['forks'] = item['forks_count']
            temp['topics'] = item['topics']
            repos.append(temp)
        return render_template('repo_results.html', repos=repos, options=options, results=results_count, p=params_g)
    elif response.status_code == 422:
        abort(422)
    else:
        abort(404)
    
    


@app.route('/trending')
def trending_repos():
    today = datetime.date.today()
    one_month_ago = today - datetime.timedelta(days=30)
    one_month_ago_str = one_month_ago.strftime("%Y-%m-%d")

    params = {
        "q": f"created:>{one_month_ago_str}",
        "sort": "stars",
        "order": "desc",
        "per_page": 8,
    }
    colors = {
            "Python": "#3776AB", # Blue
            "Java": "#B07219", # Brown
            "JavaScript": "#F7DF1E", # Yellow
            "C#": "#178600", # Green
            "C++": "#00599C", # Dark blue
            "PHP": "#777BB4", # Purple
            "R": "#198CE7", # Light blue
            "TypeScript": "#3178C6", # Cyan
            "Swift": "#FA7343", # Orange
            "C": "#438EFF", # Sky blue
            "Kotlin": "#F18E33", # Amber
            "Makefile": "#427B58", # Olive green
            "Others": "#666666" # gray 
    }
    response = requests.get("https://api.github.com/search/repositories", params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        items = data["items"]
        repos = []
        # print(f"Found {len(items)} trending repositories:")
        for item in items:
            temp = {}
            temp['name'] = item['name']
            temp['description'] = item['description']
            temp['html_url'] = item['html_url']
            temp['owner'] = item['owner']['login']
            temp['avatar'] = item['owner']['avatar_url']
            temp['language'] = item['language']
            temp['stars'] = item['stargazers_count']
            temp['forks'] = item['forks_count']
            temp['topics'] = item['topics']
            repos.append(temp)
        return render_template('trending.html', repos=repos, options=options, results=1, p=params)

    else:
        return f"Error: status code - {response.status_code}"

  


@app.route('/testing')
def testing():
    colors = {
            "Python": "#3776AB", # Blue
            "Java": "#B07219", # Brown
            "JavaScript": "#F7DF1E", # Yellow
            "C#": "#178600", # Green
            "C++": "#00599C", # Dark blue
            "PHP": "#777BB4", # Purple
            "R": "#198CE7", # Light blue
            "TypeScript": "#3178C6", # Cyan
            "Swift": "#FA7343", # Orange
            "C": "#438EFF", # Sky blue
            "Kotlin": "#F18E33", # Amber
            "Makefile": "#427B58", # Olive green
            "Others": "#666666" # gray
    }

    # default
    # return "testing"
    
    # test /users/re
    # users = [{'username': 'adamwiggins', 'avatar': '', 'html_url': 'https://github.com/adamwiggins', 'followers': 970, 'following': 16, 'bio': 'Digital toolmaker', 'location': 'Berlin', 'public_repos': 99, 'languages': [('Ruby', 70.0), ('Python', 6.67), ('Elm', 6.67), ('Others', 16.659999999999997)]}, {'username': 'emmvs', 'avatar': '', 'html_url': 'https://github.com/emmvs', 'followers': 55, 'following': 51, 'bio': 'Hey there 🤟', 'location': 'Berlin', 'public_repos': 38, 'languages': [('Ruby', 83.33), ('HTML', 6.67), ('Shell', 3.33), ('Others', 6.670000000000002)]}, {'username': 'plutov', 'avatar': '', 'html_url': 'https://github.com/plutov', 'followers': 583, 'following': 96, 'bio': 'Gopher https://www.youtube.com/packagemain', 'location': 'Berlin, Germany', 'public_repos': 53, 'languages': [('Go', 56.67), ('JavaScript', 6.67), ('Shell', 6.67), ('Others', 29.989999999999995)]}]
    # return render_template('user_results.html', users=users, colors=colors, results=20)


    # test /repos/abc
    repos = [{'name': 'abcd', 'description': None, 'html_url': 'https://github.com/nlpxucan/abcd', 'owner': 'nlpxucan', 'stars': 7640, 'forks': 596, 'topics': []}, {'name': 'abcjs', 'description': 'javascript for rendering abc music notation', 'html_url': 'https://github.com/paulrosen/abcjs', 'owner': 'paulrosen', 'stars': 1704, 'forks': 261, 'topics': ['abc-notation', 'abcjs', 'javascript', 'midi', 'music', 'music-notation', 'music-player', 'sheet-music']}, {'name': 'bitcoin-abc', 'description': 'Bitcoin ABC develops node software and infrastructure for the eCash project. This a mirror of the official Bitcoin-ABC repository.  Please see README.md', 'html_url': 'https://github.com/Bitcoin-ABC/bitcoin-abc', 'owner': 'Bitcoin-ABC', 'stars': 1126, 'forks': 720, 'topics': ['bitcoin', 'bitcoin-abc', 'ecash', 'xec']}, {'name': 'FlutterBasicWidgets', 'description': 'ABC of Flutter widgets. Intended for super beginners at Flutter. Play with 35+ examples in DartPad directly and get familiar with various basic widgets in Flutter', 'html_url': 'https://github.com/PoojaB26/FlutterBasicWidgets', 'owner': 'PoojaB26', 'stars': 864, 'forks': 286, 'topics': ['basic', 'beginner', 'dart', 'examples', 'flutter', 'playground', 'widgets']}, {'name': 'abc', 'description': 'ABC: System for Sequential Logic Synthesis and Formal Verification', 'html_url': 'https://github.com/berkeley-abc/abc', 'owner': 'berkeley-abc', 'stars': 737, 'forks': 478, 'topics': []}, {'name': 'ABCalendarPicker', 'description': 'Fully configurable iOS calendar UI component with multiple layouts and smooth animations.', 'html_url': 'https://github.com/k06a/ABCalendarPicker', 'owner': 'k06a', 'stars': 711, 'forks': 125, 'topics': []}, {'name': 'abc', 'description': 'A better Deno framework to create web application.', 'html_url': 'https://github.com/zhmushan/abc', 'owner': 'zhmushan', 'stars': 598, 'forks': 48, 'topics': ['deno', 'framework', 'http', 'server']}, {'name': 'ABCustomUINavigationController', 'description': 'Custom UINavigationController. SquaresFlips and Cube effects', 'html_url': 'https://github.com/andresbrun/ABCustomUINavigationController', 'owner': 'andresbrun', 'stars': 499, 'forks': 74, 'topics': []}, {'name': 'abc', 'description': 'Power of appbase.io via CLI, with nifty imports from your favorite data sources', 'html_url': 'https://github.com/appbaseio/abc', 'owner': 'appbaseio', 'stars': 459, 'forks': 50, 'topics': ['appbase', 'cli', 'elasticsearch', 'etl']}, {'name': 'RABCDAsm', 'description': 'Robust ABC (ActionScript Bytecode) [Dis-]Assembler', 'html_url': 'https://github.com/CyberShadow/RABCDAsm', 'owner': 'CyberShadow', 'stars': 413, 'forks': 98, 'topics': []}]
    return render_template('repo_results.html', repos=repos, results=len(repos))


    # test /trending
    # trending = [{'name': 'Startup-CTO-Handbook', 'description': "The Startup CTO's Handbook, a book covering leadership, management and technical topics for leaders of software engineering teams", 'html_url': 'https://github.com/ZachGoldberg/Startup-CTO-Handbook', 'owner': 'ZachGoldberg', 'stars': 8684, 'forks': 378, 'topics': []}, {'name': 'MemGPT', 'description': 'Teaching LLMs memory management for unbounded context 📚🦙', 'html_url': 'https://github.com/cpacker/MemGPT', 'owner': 'cpacker', 'stars': 5409, 'forks': 532, 'topics': ['chat', 'chatbot', 'gpt', 'gpt-4', 'llm', 'llm-agent']}, {'name': 'XAgent', 'description': 'An Autonomous LLM Agent for Complex Task Solving', 'html_url': 'https://github.com/OpenBMB/XAgent', 'owner': 'OpenBMB', 'stars': 4246, 'forks': 349, 'topics': []}, {'name': 'ChatGLM3', 'description': 'ChatGLM3 series: Open Bilingual Chat LLMs | 开源双语对话语言模型', 'html_url': 'https://github.com/THUDM/ChatGLM3', 'owner': 'THUDM', 'stars': 3658, 'forks': 292, 'topics': []}, {'name': 'openapi-devtools', 'description': 'Effortlessly discover API behaviour with a Chrome extension that automatically generates OpenAPI specifications in real time for any app or website', 'html_url': 'https://github.com/AndrewWalsh/openapi-devtools', 'owner': 'AndrewWalsh', 'stars': 3283, 'forks': 48, 'topics': ['api', 'chrome', 'devtools', 'generator', 'openapi', 'openapi3', 'specification']}, {'name': 'RemoveAdblockThing', 'description': 'Removes The "Ad blocker are not allowed on Youtube"', 'html_url': 'https://github.com/TheRealJoelmatic/RemoveAdblockThing', 'owner': 'TheRealJoelmatic', 'stars': 3174, 'forks': 126, 'topics': ['adblock', 'remove-not-allowed', 'tampermonkey', 'tampermonkey-userscript', 'youtube']}, {'name': 'semana-javascript-expert08', 'description': 'JS Expert Week 8.0 - 🎥Pre processing videos before uploading in the browser 😏', 'html_url': 'https://github.com/ErickWendel/semana-javascript-expert08', 'owner': 'ErickWendel', 'stars': 2523, 'forks': 1778, 'topics': ['demuxer', 'javascript', 'mp4', 'mp4box', 'muxer', 'video-processing', 'video-streaming', 'webcodecs', 'webm', 'webstream', 'webworker', 'workers']}, {'name': 'Wonder3D', 'description': 'A cross-domain diffusion model for 3D reconstruction from a single image', 'html_url': 'https://github.com/xxlong0/Wonder3D', 'owner': 'xxlong0', 'stars': 2008, 'forks': 110, 'topics': ['3d-aigc', '3d-generation', 'single-image-to-3d']}, {'name': 'smallchat', 'description': 'A minimal programming example for a chat server', 'html_url': 'https://github.com/antirez/smallchat', 'owner': 'antirez', 'stars': 1990, 'forks': 159, 'topics': []}, {'name': 'go-ethereum', 'description': 'Forked Golang execution layer implementation of the Ethereum protocol.', 'html_url': 'https://github.com/SidraChain/go-ethereum', 'owner': 'SidraChain', 'stars': 1759, 'forks': 491, 'topics': []}, {'name': 'sidra-contracts', 'description': 'Genesis Smart Contracts for Sidra Chain', 'html_url': 'https://github.com/SidraChain/sidra-contracts', 'owner': 'SidraChain', 'stars': 1640, 'forks': 517, 'topics': []}, {'name': 'fadblock', 'description': 'Friendly Adblock for YouTube: A fast, lightweight, and undetectable YouTube Ads Blocker for Chrome, Opera and Firefox.', 'html_url': 'https://github.com/0x48piraj/fadblock', 'owner': '0x48piraj', 'stars': 1601, 'forks': 49, 'topics': ['adblock', 'adguard', 'blocker', 'chrome', 'extension', 'firefox', 'javascript', 'opera', 'privacy', 'youtube']}, {'name': 'flexoki', 'description': 'An inky color scheme for prose and code.', 'html_url': 'https://github.com/kepano/flexoki', 'owner': 'kepano', 'stars': 1233, 'forks': 38, 'topics': ['alacritty', 'color', 'color-scheme', 'colors', 'iterm2', 'iterm2-color-scheme', 'kitty', 'neovim', 'neovim-colorscheme', 'terminal-colors', 'theme', 'vscode', 'vscode-theme', 'wezterm', 'wezterm-colorscheme', 'xresources']}, {'name': 'text-embeddings-inference', 'description': 'A blazing fast inference solution for text embeddings models', 'html_url': 'https://github.com/huggingface/text-embeddings-inference', 'owner': 'huggingface', 'stars': 1175, 'forks': 37, 'topics': ['ai', 'embeddings', 'huggingface', 'llm', 'ml']}, {'name': 'DreamCraft3D', 'description': 'Official implementation of DreamCraft3D: Hierarchical 3D Generation with Bootstrapped Diffusion Prior', 'html_url': 'https://github.com/deepseek-ai/DreamCraft3D', 'owner': 'deepseek-ai', 'stars': 1081, 'forks': 31, 'topics': ['3d-creation', '3d-generation', 'aigc', 'diffusion-models', 'generative-model', 'image-to-3d']}, {'name': '4K4D', 'description': '4K4D: Real-Time 4D View Synthesis at 4K Resolution', 'html_url': 'https://github.com/zju3dv/4K4D', 'owner': 'zju3dv', 'stars': 1080, 'forks': 23, 'topics': []}, {'name': 'Sistema-Anti-Fraude-Electoral', 'description': 'Sistema Open Source para Identificar potenciales fraudes electorales, minimizar su ocurrencia e impacto.', 'html_url': 'https://github.com/Las-Fuerzas-Del-Cielo/Sistema-Anti-Fraude-Electoral', 'owner': 'Las-Fuerzas-Del-Cielo', 'stars': 1076, 'forks': 185, 'topics': []}, {'name': 'geist-font', 'description': None, 'html_url': 'https://github.com/vercel/geist-font', 'owner': 'vercel', 'stars': 1045, 'forks': 24, 'topics': ['font', 'variable-fonts']}, {'name': 'distil-whisper', 'description': None, 'html_url': 'https://github.com/huggingface/distil-whisper', 'owner': 'huggingface', 'stars': 962, 'forks': 20, 'topics': ['audio', 'speech-recognition', 'whisper']}, {'name': 'zero123plus', 'description': 'Code repository for Zero123++: a Single Image to Consistent Multi-view Diffusion Base Model.', 'html_url': 'https://github.com/SUDO-AI-3D/zero123plus', 'owner': 'SUDO-AI-3D', 'stars': 921, 'forks': 59, 'topics': ['3d', '3d-graphics', 'aigc', 'diffusers', 'diffusion-models', 'image-to-3d', 'research-project', 'text-to-3d']}]
    # return render_template('trending_repos.html', repos=trending)



if __name__ == '__main__':
    app.run(debug=True)


# limitation
"""
{
    "message": "Only the first 1000 search results are available",
    "documentation_url": "https://docs.github.com/v3/search/"
}
"""

