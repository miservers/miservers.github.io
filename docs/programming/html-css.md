---
layout: default
title: HTML - CSS
parent: Programming
nav_order: 1
---


### CSS Selector
**ID Selectors (#)** : The CSS rule below will be applied to the HTML element with id="myp1": 

~~~
#myp1 {
  text-align: center;
  color: red;
}

<p id="myp1"> ip op </p>
~~~

**Class Selectors (.)**: applied on all HTML elements with class="prodtab" 

~~~
.prodtab {
  text-align: center;
  color: red;
}

<p class="prodtab">Red and cen.</p> 
~~~

* `.class1 .class2` : example .name1 .name2 Selects all elements with name2 that is a descendant of an element with name1    
* `element.class` : example p.intro   Selects all <p> elements with class="intro"  
* `:hover` : example  a:hover Selects links on mouse over  
* `:focus` : example  input:focus Selects the input element which has focus  
* `:checked` : example  input:checked Selects every checked <input> element  

See:  https://www.w3schools.com/cssref/css_selectors.asp



### Center a block or image
~~~
p.centredtext {
    margin-left: auto;
    margin-right: auto; 
}
...
<p class="entredtext">This a centrer text... </p>
~~~

### Bootstrap 4
**BS4 Demos**: [bootstrap-demo.html](../java-workspace/html-css-lab/bootstrap-demo.html)

**Container**: Bootstrap requires a containing element to wrap site contents.
~~~html
<div class="container">
  your html
</div>
~~~

**Bootstrap 4 Grid System** is built with flexbox and allows up to **12 columns** across the page. **col-sm-2** equal to 2 columns for smal device.  
Format : col-a-b, a=sm,lg,xl devices. b=1 to 12 columns.   
col-*: can't collapse   
col-sm-*: may collapse    

~~~html
<div class="row  pt-2">
  <div class="col-sm-2">
    <label for="username">Username</label>
  </div>
  <div class="col-sm-6">
    <input type="text" class="form-control" id="username" name="username"></input>
  </div>  
</div>
~~~

**Bootstrap 4 Utilities**: Bootstrap 4 has a lot of utility/helper classes to quickly style elements without using any CSS code. See : https://www.w3schools.com/bootstrap4/bootstrap_utilities.asp.  Examples below.


**Spacing**: Format : {property}{sides}-{size}. Example **pt-2** stand for : padding top 2(=8px)  
See https://www.w3schools.com/bootstrap4/bootstrap_utilities.asp

**Text center** : class="text-center"

**Center Align**: .mx-auto class


**Border** class: border, border-0, border-top-0. border Colors: border-primary, border-success,etc. Borders radius: rounded, rounded-circle,...

**Width**: w-50 = width of 50%




### Responsive Table using div
See [div-table.html](../java-workspace/html-css-lab/div-table.html)

### Flexbox guide
[Excellent article on CSS](https://css-tricks.com/snippets/css/a-guide-to-flexbox/#flexbox-background)


