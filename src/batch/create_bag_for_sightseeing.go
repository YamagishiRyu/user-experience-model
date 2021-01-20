package main

import (
	"encoding/csv"
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
	"time"
)

const layout = "2006-01-02 15:04:05.0"

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
		writeIDs(city)
	}

}

func writeIDs(cityName string) {
	var userBag map[string]int = make(map[string]int)
	var placeBag map[string]int = make(map[string]int)
	var tagBag map[string]int = make(map[string]int)

	var ids_file_path = "./data/" + cityName + ".csv"
	ids_file, err := os.Open(ids_file_path)
	if err != nil {
		fmt.Println("ids file not found")
		return
	}
	defer ids_file.Close()
	reader := csv.NewReader(ids_file)

	outputFileName := "data/ids/id-" + cityName + ".csv"
	outputFile, err := os.OpenFile(outputFileName, os.O_WRONLY|os.O_CREATE, 0600)
	if err != nil {
		fmt.Println("output file not found")
	}
	defer outputFile.Close()
	writer := csv.NewWriter(outputFile)
	defer writer.Flush()

	var row []string

	var writeRows [][]string
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

		identifier := row[0]
		userId := checkBag(row[1], &userBag)

		t, err := time.Parse(layout, row[2])
		if err != nil {
			fmt.Println(err)
		}
		month := strconv.Itoa(int(t.Month()) - 1)

		placeId := checkBag(row[3], &placeBag)

		var tags []int
		for _, t := range strings.Split(row[4], ",") {
			tags = append(tags, checkBag(t, &tagBag))
		}

		writeRow := []string{
			identifier,
			strconv.Itoa(userId),
			month,
			strconv.Itoa(placeId),
			strings.Trim(strings.Join(strings.Fields(fmt.Sprint(tags)), ","), "[]"),
		}

		writeRows = append(writeRows, writeRow)
	}
	writer.WriteAll(writeRows)

	writeBag("data/bags/user-"+cityName+".csv", &userBag)
	writeBag("data/bags/place-"+cityName+".csv", &placeBag)
	writeBag("data/bags/tag-"+cityName+".csv", &tagBag)
}

func checkBag(item string, bag *map[string]int) int {
	i, ok := (*bag)[item]
	if ok {
		return i
	} else {
		id := len(*bag)
		(*bag)[item] = id
		return id
	}
}

func writeBag(fileName string, bag *map[string]int) {
	file, err := os.OpenFile(fileName, os.O_WRONLY|os.O_CREATE, 0600)
	if err != nil {
		fmt.Println(fileName + " output file not found")
	}
	defer file.Close()
	writer := csv.NewWriter(file)

	for k, v := range *bag {
		writer.Write([]string{
			k,
			strconv.Itoa(v),
		})
		writer.Flush()
	}
}
