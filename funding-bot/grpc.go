package fbot

import (
	"context"
	"crypto/tls"
	"fmt"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials"
	"google.golang.org/grpc/credentials/insecure"
)

func GetGRPCConnection() *grpc.ClientConn {
	var creds credentials.TransportCredentials
	if config.GrpcInsecure {
		creds = insecure.NewCredentials()
	} else {
		creds = credentials.NewTLS(&tls.Config{})
	}

	options := []grpc.DialOption{
		grpc.WithBlock(),
		grpc.WithTransportCredentials(creds),
	}
	ctx, _ := context.WithTimeout(context.Background(), time.Minute)

	conn, err := grpc.DialContext(ctx, config.GrpcUrl, options...)
	if err != nil {
		fmt.Printf("Cannot connect to gRPC endpoint %s\n", config.GrpcUrl)
		panic(err)
	}

	return conn
}
