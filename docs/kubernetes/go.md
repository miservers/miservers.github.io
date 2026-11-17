

## Types
Avec type — un nouveau type réutilisable
```go
type Pod struct {
    Name     string
    Replicas int
}
```

Utilisation
```go
var p Pod
p1 := Pod{Name: "httpd"}
p2 := &Pod{Name: "nginx"}
```

**Avantage — attacher des méthodes**

Sans type → impossible d'attacher une méthode à int
```go
type Port int

func (p Port) IsHTTPS() bool {
    return p == 443
}

var p Port = 443
fmt.Println(p.IsHTTPS())  // true
```

## Tags Go

### Syntaxe
```go
NomChamp Type `clé:"valeur"`
```

### Règles
- Délimiteur : backticks `` ` ``
- Position : après le type du champ
- Ignoré par le compilateur
- Lu par les bibliothèques via réflexion

### Options JSON
- `json:"name"` → renomme le champ
- `json:"name,omitempty"` → omis si vide/zéro
- `json:"-"` → toujours ignoré

### Exemple de Tag
```go
type Pod struct {
    Name     string `json:"name"`
    Replicas int32  `json:"replicas,omitempty"`
    Internal string `json:"-"`
    Image    string `json:"image" yaml:"image"`
    Database string `db:"db_name"`
}

p := Pod{Name: "httpd", Replicas: 0, Internal: "secret"}
json.Marshal(p)
// → {"name":"httpd"}
// Replicas omis (omitempty + valeur 0)
// Internal omis (-)
```