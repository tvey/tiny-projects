package main

import (
    "bufio"
    "fmt"
    "log"
    "math/rand"
    "os"
    "time"
)

func main() {
    file, err := os.Open("movies.txt")
    if err != nil {
        log.Fatal(err)
    }

    scanner := bufio.NewScanner(file)
    scanner.Split(bufio.ScanLines)
    var movies []string

    for scanner.Scan() {
        movies = append(movies, scanner.Text())
    }

    file.Close()
    
    rand.Seed(time.Now().Unix()) 

    movie := movies[rand.Intn(len(movies))]

    fmt.Println("Случайный фильм:", movie)
}
