
default:
	landslide -i -l no -t theme -r pyjs.md 

pdf: default
	prince presentation.html -s theme/css/pdf.css -o pyjs.pdf
	
