i=1
while true; do
  curl -X POST http://localhost:8000/order \
    -H "Content-Type: application/json" \
    -d "{\"order_id\": $i, \"user_id\": 42, \"items\": [\"item$i\"]}"
  echo " → Sent order #$i"
  i=$(expr $i + 1)
  sleep 3
done
