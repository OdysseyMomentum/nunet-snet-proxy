FUNC_TYPE=$1
ARG_2=$2
ARG_3=$3
ARG_4=$4
ARG_5=$5

IDENTITY_NAME=$ARG_2
EMAIL_PK=$ARG_3


getScore(){
    CHANNEL_ID=$ARG_2
    SERVICE_ID=$ARG_5
    ORGANIZATION_ID="odyssey-org"
    URL=$ARG_3
    BODY="ajgkaj"
    snet client call --channel-id $CHANNEL_ID $ORGANIZATION_ID $SERVICE_ID  default_group fn_score_calc '{"headline":"'$URL'","body":"'$BODY'"}' -y
}


case $FUNC_TYPE in
    get_score) getScore ;;
    
esac