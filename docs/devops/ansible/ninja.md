### Ninja 2
https://python-web.teclado.com/section09/lectures/08_jinja2_tests/

#### Delimiters
{% ... %} for Statements

{{ ... }} for Expressions to print to the template output

{# ... #} for Comments not included in the template output

#### Tests
Syntax:  var **is** Test

{% set n = 10 %}

{% if n is divisibleby(2) and n is divisibleby(3) %}
  <p>It's even!</p>
{% endif %}

#### Variables
The following lines do the same thing:

{{ foo.bar }}
{{ foo['bar'] }}

#### Filters
{{ name|striptags|title }} 
