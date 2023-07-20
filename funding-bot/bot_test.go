package fbot_test

import (
	"bufio"
	"fbot"
	"fmt"
	"os"
	"strings"
	"testing"

	sdk "github.com/cosmos/cosmos-sdk/types"
	"github.com/stretchr/testify/require"
)

func TestIsPosAgainstMarket(t *testing.T) {

	for _, tc := range []struct {
		name      string
		posSize   sdk.Dec
		mark      sdk.Dec
		index     sdk.Dec
		isAgainst bool
	}{
		{
			name:    "pos long, mark < index",
			posSize: sdk.NewDec(10), mark: sdk.NewDec(10), index: sdk.NewDec(20), isAgainst: true},
		{
			name:    "pos long, mark > index",
			posSize: sdk.NewDec(10), mark: sdk.NewDec(20), index: sdk.NewDec(10), isAgainst: false},
		{
			name:    "pos short, mark < index",
			posSize: sdk.NewDec(-10), mark: sdk.NewDec(10), index: sdk.NewDec(20), isAgainst: false},
		{
			name:    "pos short, mark > index",
			posSize: sdk.NewDec(-10), mark: sdk.NewDec(20), index: sdk.NewDec(10), isAgainst: true},
	} {
		t.Run(tc.name, func(t *testing.T) {
			require.Equal(t, tc.isAgainst, fbot.IsPosAgainstMarket(tc.posSize, tc.mark, tc.index))
		})

	}
}

func TestSetupLoggingFile(t *testing.T) {
	filename := "temp-test"
	if _, err := os.Stat(filename); err == nil {
		err := os.Remove(filename)
		require.NoError(t, err)
	}

	fbot.SetupLoggingFile(filename)
	file, err := os.Open(filename)
	defer file.Close()
	require.NoError(t, err)

	var hasExpectedContent bool
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		if strings.Contains(line, fmt.Sprintf("logger name: %v", filename)) {
			hasExpectedContent = true
		}
	}

	err = scanner.Err()
	require.NoError(t, err)
	require.True(t, hasExpectedContent)

	require.NoError(t, os.Remove(filename))
}
