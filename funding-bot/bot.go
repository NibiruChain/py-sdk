package fbot

import (
	"github.com/NibiruChain/nibiru/app"
	perp "github.com/NibiruChain/nibiru/x/perp/v2/types"
	sdk "github.com/cosmos/cosmos-sdk/types"
	"log"
	"os"
)

var _ = app.BankModule.Name

type PositionState struct {
	Size   sdk.Dec
	Margin sdk.Dec
	Upnl   sdk.Dec
	Block  int64
	Trader sdk.AccAddress
}

var LOGGING_FILE = "test-log.txt"

func LoggingFilename() string {

	// TODO  Specify the logging file name with a command line arg
	// if os.Arg...
	// TODO  Specify the logging file name with a config variable
	return LOGGING_FILE
}

// Initializes a logging file with the given file name.
func SetupLoggingFile(loggingFilename string) {

	// Make blank file
	file, err := os.Create(loggingFilename)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	log.SetOutput(file)
	log.Printf("logger name: %v", loggingFilename)
}

// IsPosAgainstMarket returns true if the position is diverging the mark and
// index price. In other words, it returns true if the trader is paying funding
// on this position rather than receiving it.
func IsPosAgainstMarket(posSize sdk.Dec, mark sdk.Dec, index sdk.Dec) bool {
	marketLong := mark.GT(index)
	posLong := posSize.IsPositive()
	return marketLong != posLong
}

func SomethingCool() {
	// TODO need GRPC client

	// grpcClientConnection := GetGRPCConnection()
	// var querierPerp = perp.NewQueryClient(grpcClientConnection)
	// marketsResp, err := querierPerp.QueryMarkets()
	// x := marketsResp.AmmMarkets[0]
	// x.Amm.Bias()
}
