### Ninja 2

https://python-web.teclado.com/section09/lectures/08_jinja2_tests/

#### Delimiters
{% raw %}

{% ... %} for Statements

{{ ... }} for Expressions to print to the template output

{# ... #} for Comments not included in the template output

{% endraw %}

#### Tests
Syntax:  var **is** Test

{% raw %}
~~~html
{% set n = 10 %}

{% if n is divisibleby(2) and n is divisibleby(3) %}
  <p>It's even!</p>
{% endif %}
~~~
{% endraw %}

#### Variables
The following lines do the same thing:

{% raw %}
{{ foo.bar }}
{{ foo['bar'] }}
{% endraw %}

#### Filters

{% raw %}
{{ name|striptags|title }} 
{% endraw %}