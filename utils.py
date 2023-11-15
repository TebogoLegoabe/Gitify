""" this is not 100% accurate result of language percentages
    use none lite versions for more accurate results
"""
import requests
from os import getenv
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


def get_languages_lite(api_url):
    """ it returns lanugage usage percentage of repositories using main languages
    NOTE: does only one request and is not 100% accurate
    USAGE: get_languages_lite("https://api.github.com/users/{user_name}/repos") # repositories url

    """
    # gets all repositories of the user
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        repos = response.json()
        language_counts = {}
        language_percentages = {}
        # loops over the list of repositories and gets the main language used in that repo
        for repo in repos:
            language = repo["language"]
            if language is not None:
                language_counts[language] = language_counts.get(language, 0) + 1
        total_repos = len(repos)

        # language_count = {'JavaScript': 23, 'HTML': 1, 'Dart': 1, 'ActionScript': 1, 'CoffeeScript': 1, 'TypeScript': 1, 'PHP': 1}
        # loops over the list of counted languages and calculates their percentage relative to the other languages
        for language, count in language_counts.items():
            percentage = round(count / total_repos * 100, 2)
            language_percentages[language] = percentage
        # returns the language as dictionary
        # language_percentages = {'JavaScript': 76.67, 'HTML': 3.33, 'Dart': 3.33, 'ActionScript': 3.33, 'CoffeeScript': 3.33, 'TypeScript': 3.33, 'PHP': 3.33}
        return language_percentages


def get_language_percentage_one_repo_lite(api_url):
    """ gets the langauges percentages of the given repo
        USAGE:  get_language_percentage_one_repo_lite("https://api.github.com/repos/{repository_name}/{user_name}/languages")
    """
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        languages = response.json()
        language_percentages = {}
        total_bytes = sum(languages.values())

        # Loop through each language and its bytes calculates their percentage
        for language, bytes in languages.items():
            percentage = round(bytes / total_bytes * 100, 2)
            language_percentages[language] = percentage
        return language_percentages
    else:
        return None




def get_langauge_percentage(api_url="https://api.github.com/users/krasimir"):
    """ returns the percentage usages of languages of all repositories"""
    api_url = api_url + "/repos"
    response = requests.get(api_url)
    if response.status_code == 200:
        repos = response.json()
    else:
        print(f"Error: {response.status_code}")
    
    languages = {}
    for res in repos:
        temp = get_language_usage(res['languages_url'])
        for t in temp:
            languages[t] = temp[t] + languages[t] if t in languages else temp[t]

    language_percentages = {}
    total_bytes = sum(languages.values())

    # Loop through each language and its bytes and calculate thier percentage
    for language, bytes in languages.items():
        percentage = round(bytes / total_bytes * 100, 2)
        language_percentages[language] = percentage

    return language_percentages


if __name__ == "__main__":
    print("--------------------------------------")
    print(get_language_percentage_one_repo_lite("https://api.github.com/repos/creytiv/re/languages"))
    print("--------------------------------------")
    print(get_languages_lite("https://api.github.com/users/krasimir/repos"))
    print("-------------------------------------")
    get_langauge_percentage("https://api.github.com/users/krasimir")
