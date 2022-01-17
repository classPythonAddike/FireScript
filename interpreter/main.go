package main

import (
	"log"
	"os"

	"github.com/urfave/cli/v2"
)

func main() {
    app := &cli.App{
        Name: "FscRun",
        Usage: "Run an fsc file",
        Commands: []*cli.Command{
            {
                Name: "run",
                Aliases: []string{"r"},
                Usage: "Run a .fsc file",
                Flags: []cli.Flag{
                    &cli.StringFlag{
                        Name: "file",
                        Aliases: []string{"f"},
                        Usage: "Specify file to run",
                    },
                },
                Action: func(c *cli.Context) error {
                    parser := NewParser(c.String("file"))
                    parser.ParseBytecode()

                    for {
                        parser.instructions[parser.pointer]()
                        parser.pointer += 1
                    }
                },
            },
        },
    }

    err := app.Run(os.Args)

    if err != nil {
        log.Fatal(err)
    }
}
