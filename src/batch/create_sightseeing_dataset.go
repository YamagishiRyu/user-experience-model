package main

import (
	"encoding/csv"
	"fmt"
	"io"
	"os"
	"regexp"
	"strings"

	"github.com/cheggaaa/pb/v3"
)

const (
	identifierIndexInDataset = 1
	userIndexInDataset       = 3
	timeIndexInDataset       = 5
)

const (
	cityDataFilePrefix           = "./data/user_visits/userVisits-"
	identifierIndexInCityDataset = 0
	poiIndexInCityDataset        = 3
)

const (
	identifierIndexInSceneDataset  = 0
	sceneStringINdexInSceneDataset = 2
)

type UserTime struct {
	userId string
	time   string
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

	var userBag map[string]UserTime = make(map[string]UserTime)
	collectUserAndTime("./data/flickr/sightseeing_dataset.csv", &userBag)

	var sceneBag map[string]string = make(map[string]string)
	collectSceneString("./data/sightseeing_place.csv", &sceneBag)

	for _, dataFile := range dataFiles {
		writeData(dataFile, &userBag, &sceneBag)
	}
}

func collectUserAndTime(dataset_file_name string, bag *map[string]UserTime) {
	file, err := os.Open(dataset_file_name)
	if err != nil {
		fmt.Println("ids file not found")
		return
	}
	defer file.Close()
	reader := csv.NewReader(file)

	var row []string
	for {
		row, err = reader.Read()
		if err == io.EOF {
			fmt.Println("dataset read done.")
			break
		} else if err != nil {
			fmt.Println(err)
			fmt.Println("can not read dataset csv")
			break
		}

		(*bag)[row[identifierIndexInDataset]] = UserTime{userId: row[userIndexInDataset], time: row[timeIndexInDataset]}
	}
}

func collectSceneString(fileName string, sceneBag *map[string]string) {
	file, err := os.Open(fileName)
	if err != nil {
		fmt.Println("scene file not found")
		return
	}
	defer file.Close()
	reader := csv.NewReader(file)

	var row []string
	tagPattern := regexp.MustCompile(`(.*):`)
	bar := pb.StartNew(134269)
	for {
		row, err = reader.Read()
		if err == io.EOF {
			fmt.Println("scene read done.")
			break
		} else if err != nil {
			fmt.Println(err)
			fmt.Println("can not read scene data")
			continue
		}

		sceneString := row[sceneStringINdexInSceneDataset]
		sceneWithProbs := strings.Split(sceneString, ",")[:5]
		var scenes []string
		for _, t := range sceneWithProbs {
			ms := tagPattern.FindStringSubmatch(t)
			if len(ms) <= 1 {
				fmt.Println("regex error", row[identifierIndexInSceneDataset])
			}
			scenes = append(scenes, ms[1])
		}
		(*sceneBag)[row[identifierIndexInSceneDataset]] = strings.Join(scenes, ",")
		bar.Increment()
	}
}

func writeData(cityName string, userBag *map[string]UserTime, sceneBag *map[string]string) {
	fileName := cityDataFilePrefix + cityName + ".csv"
	file, err := os.Open(fileName)
	if err != nil {
		fmt.Println("city file not found")
		return
	}
	defer file.Close()
	reader := csv.NewReader(file)
	reader.Comma = ';'

	outputFileName := "data/" + cityName + ".csv"
	outputFile, err := os.OpenFile(outputFileName, os.O_WRONLY|os.O_CREATE, 0600)
	if err != nil {
		fmt.Println(outputFileName + " output file not found")
	}
	defer outputFile.Close()
	writer := csv.NewWriter(outputFile)

	var row []string
	_, err = reader.Read() // header
	if err != nil {
		fmt.Println(err)
		fmt.Printf("can not read city data csv: %s", cityName)
	}
	for {
		row, err = reader.Read()
		if err == io.EOF {
			fmt.Printf("city(%s) done.", cityName)
			break
		} else if err != nil {
			fmt.Println(err)
			fmt.Printf("can not read city data csv: %s", cityName)
			break
		}

		identifier := row[identifierIndexInCityDataset]
		sceneString, ok := (*sceneBag)[identifier]
		if ok {
			writer.Write([]string{
				identifier,                    // identifier
				(*userBag)[identifier].userId, // user id
				(*userBag)[identifier].time,   // time
				row[poiIndexInCityDataset],    // poi
				sceneString,                   //  scenes(count: 5)
			})
			writer.Flush()
		}
	}
}
