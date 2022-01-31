#!/usr/bin/bash

region=europe-west1
runtime=python39
func_name=document-generator
entrypoint=generate_document


gcloud functions deploy $func_name --entry-point=$entrypoint --runtime $runtime --trigger-http --region $region --allow-unauthenticated
