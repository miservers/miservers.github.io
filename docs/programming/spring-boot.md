---
layout: default
title: Spring Boot
parent: Programming
nav_order: 4
---

### Spring MVC
![](/docs/images/java/spring-mvc.png)

### RESTful with Jpa dependencies
 * spring-boot-starter-web
 * spring-boot-starter-data-jpa
 * spring-boot-starter-validation 

### Conventions
**Structure**

~~~
      +- lab
          |
          +- spring
               +- Application.java
               |
               +- user
                   +- User.java
                   +- UserController.java
                   +- UserRepo.java
               |
               +- product
                   +- Product.java
                   +- ProductController.java
                   +- ProductRepo.java
               
~~~

Application.java

~~~java
@SpringBootApplication
@ComponentScan
@EntityScan
@EnableJpaRepositories
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
...
~~~

**Scan** : if *Application.java* is not placed in the top, you must point out where to scan components

~~~java
@SpringBootApplication
@ComponentScan(basePackages = {"lab.spring.controller", "lab.spring.exception", })
@EntityScan("lab.spring.model")
@EnableJpaRepositories("lab.spring.repo")
public class Application {

	public static void main(String[] args) {
...
~~~


### Annotations
 * `@ModelAttribute`: one of the most important Spring annotations. It bind method parameters or return to a named Model bean.

 *`@Data`: is a Lombok annotation to create all the getters, setters, equals, hash, and toString

### Spring validation
pom.xml  

~~~xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-validation</artifactId>
</dependency>
~~~

For example  **@Email** annotation  throw exception if email is not valid.

~~~java
@Entity
public class User {

    @NotBlank          // validator
    String username;

    @Email(message = "email bad format")  //validator
    String email;

    ...
~~~



### Hot deployment/reload
Add this dependency to pom.xml

~~~ xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-devtools</artifactId>
    <optional>true</optional>
</dependency>
~~~

### Submit POST
2 ways. EITHER you use **application/json** request, in this case you get benefits from @RequestBody to map you model. OR use x-www-form... like below. In both case client must specify **Content-Type** in its header. 

~~~java   
    @PostMapping(consumes = MediaType.APPLICATION_JSON_VALUE) 
    public ResponseEntity<?> create(@RequestBody User user)  {
        userDao.save(user);
        return ResponseEntity.ok("user created");
    }

    @PostMapping(value = "/creawithform", consumes = "application/x-www-form-urlencoded") 
    public ResponseEntity<?> create2(User user)  {
        userDao.save(user);
        return ResponseEntity.ok("user created");
    }
~~~


### Spring boot with H2 database
[spring-boot-h2-database](https://www.baeldung.com/spring-boot-h2-database)

### Logging with Lombok
 * **@Log4j2** – Creates the logger with following statement:

~~~java
private static final org.apache.logging.log4j.Logger log = 
    org.apache.logging.log4j.LogManager.getLogger(LogExample.class);
~~~

 * **@Slf4j** – Creates the logger with following statement:

~~~java
Creates private static final org.slf4j.Logger log = 
    org.slf4j.LoggerFactory.getLogger(LogExample.class);
~~~

Usage :

~~~java
@Slf4j
public class MyClass 
{
    public void myFunc() {
        log.info("Simple log statement with inputs {}, {} and {}", 1, 2, 3);
    }
}
~~~

**pom.xml**:

~~~xml
<dependency>
    <groupId>org.projectlombok</groupId>
    <artifactId>lombok</artifactId>
</dependency>
~~~

### Exception managmenent
Use **@ControllerAdvice** and **@ExceptionHandler**

Example: **spring-boot-lab**

### Junit of RestFul api
with **TestRestTemplate** 

**Annotations**: @RunWith, @SpringBootTest, @LocalServerPort, 

**Beans** : TestRestTemplate, UriComponentsBuilder, ResponseEntity, HttpEntity, HttpHeaders

Example:  **UserControllerTest.java** in **spring-boot-lab**

https://howtodoinjava.com/spring-boot2/testing/testresttemplate-post-example/

~~~java
@Test
public
void testGetAllUsers()  {
	ResponseEntity<String> response = restTemplate.getForEntity(uri.getPath(), String.class);
	
	assertEquals(200, response.getStatusCodeValue());
	System.out.println("All Users: " + response.getBody());
	
}
~~~

### Pagination
Example of RestFul service:  
Url : http://localhost:8080/api/patient?pageNo=0&pageSize=5&sortBy=id

~~~java
@GetMapping()
public List<Patient>  all(@RequestParam Integer pageNo,
                          @RequestParam Integer pageSize,
                          @RequestParam(defaultValue = "id") String  sortBy    ) {

    Pageable paging = PageRequest.of(pageNo, pageSize, Sort.by(sortBy));
    Page<Patient> result  = patientRepo.findAll(paging);
    if (result.hasContent())
        return result.getContent();
    else 
        return new ArrayList<Patient>();
}
~~~
 
### Query derivation mechanism in Spring Data JPA.

With zero implementation, only declare method with theses keywords in the Repository interface:  
   **ByFieldName,  Top3By, Is, IsNot, IsNotNull, True, False, StartingWith, Containing, Like, OrderBy, Asc/Desc** 
   
[Query Creation](https://docs.spring.io/spring-data/jpa/docs/current/reference/html/#jpa.query-methods.query-creation)

Examples:  

~~~java
@Repository
public interface UserRepo extends JpaRepository<User, Long>{
  List<User> findByName(String name);
  List<User> findTop3ByAge();
  List<User> findByProfesionEquals(String prof);
  List<User> findByNameIs(String name);
  List<User> findByNameIsNot(String name);
  List<User> findByNameIsNull();
  List<User> findByNameIsNotNull();
  
  List<User> findByAgeGreaterThanEqual(Integer age);
  
  List<User> findByActiveTrue();
  List<User> findByActiveFalse();
  
  List<User> findByNameStartingWith(String prefix);
  List<User> findByNameContaining(String infix);
  List<User> findByNameLike(String likePattern);
  
} 
~~~
  

### RESTful web service
Conventions:
 * **GET**: Read.   
   **GET /product** get all products. **GET /product/{id}** read product identified  by id. return **HTTP 200(OK)** status.  if resource identified by ID cannot be found, an **HTTP 404** status is returned. 
 * **POST**: Create.  
   **POST  /product** create the product transmitted. And return created Id in response, and **HTTP 201 (Created)** status .
 * **PUT**: Update.  
   **PUT /product/{id}** update product identified by id with that transmitted. If resource not found , an **HTTP 404** status is returned. if found return **HTTP 200(OK)** in response
 * **DELETE**: Delete.   
   **DELETE /product/{id}**. If it doesn't exist, an **HTTP 404** status is returned. If it exists, it is deleted, and an **HTTP 204** (No Content) status is returned.
Les web services Rest are resources. a resource is identified by its domain name: product, bill, order, etc. 

 
### Hard Errors
 * Has been blocked by CORS policy  No 'Access-Control-Allow-Origin' header is present  
   ==> Add **@CrossOrigin** on the spring controller class. 
 * WebKitFormBoundaryea4RZF1zatntX5RT;charset=UTF-8' not supported"
   ==> Use `@ModelAttribute` instead of `@RequestBody`
   ~~~
   @PostMapping() 
    public ResponseEntity<?> create(@ModelAttribute Patient patient)  {
        ....
   ~~~

 * 

### Tools
  * **RestMan** : opera extension to build http request
  * **Postman**: HTTP requests builder. To test your API



### References
 * https://howtodoinjava.com/spring-boot/


 



