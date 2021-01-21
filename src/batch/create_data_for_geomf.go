package main

import (
	"encoding/csv"
	"fmt"
	"io"
	"os"
	"strconv"
	"time"
)

type UserPlace struct {
	userId  string
	placeId string
}

func main() {
	var dataFiles = []string{
		"Buda-allPOI",
		"Delh-allPOI",
		"Edin",
		"Glas",
		"Osak",
		"Pert-allPOI",
		"Toro",
		"Vien-allPOI",
	}

	for _, city := range dataFiles {
		countVisit(city)
	}
}

func countVisit(cityName string) {
	var visits map[UserPlace]int = make(map[UserPlace]int)

	idFileName := "./data/sightseeing/ids/id-" + cityName + ".csv"
	ids_file, err := os.Open(idFileName)
	if err != nil {
		fmt.Println("ids file not found")
		return
	}
	defer ids_file.Close()
	reader := csv.NewReader(ids_file)

	var row []string
	for {
		row, err = reader.Read()
		if err == io.EOF {
			fmt.Printf("Ids file DONE: %s\n", cityName)
			time.Sleep(time.Second)
			break
		} else if err != nil {
			fmt.Println(err)
			fmt.Println("can not read dataset csv")
			break
		}

		ul := UserPlace{userId: row[1], placeId: row[3]}
		visits[ul]++
	}
	writeVisits("./data/sightseeing/geomf/data-"+cityName+".txt", &visits)
}

func writeVisits(fileName string, bag *map[UserPlace]int) {
	file, err := os.OpenFile(fileName, os.O_WRONLY|os.O_CREATE, 0600)
	if err != nil {
		fmt.Println(fileName + " output file not found")
	}
	defer file.Close()
	writer := csv.NewWriter(file)
	writer.Comma = '\t'

	for k, v := range *bag {
		writer.Write([]string{
			k.userId,
			k.placeId,
			strconv.Itoa(v),
		})
	}
	writer.Flush()
}
