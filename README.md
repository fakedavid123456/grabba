# Technical Challenge

## Part 1 - simple spider
```bash
scrapy crawl simplespider \
    -s LOG_LEVEL=INFO \
    -s CLOSESPIDER_ITEMCOUNT=300 \
    -o output/theurge.jl
```

## Part 2 - yaml-driven spider
```bash
scrapy crawl yamlspider \
    -s LOG_LEVEL=INFO \
    -s CLOSESPIDER_ITEMCOUNT=300 \
    -a config=configs/theurge.yaml \
    -o output/theurge.jl
```
## Part 3 - logging download latency
```bash
scrapy crawl yamlspider \
    -s LOG_LEVEL=INFO \
    -s CLOSESPIDER_ITEMCOUNT=300 \
    -s DOWNLOAD_LATENCY_ENABLED=True \
    -a config=configs/theurge.yaml \
    -o output/theurge.jl
```
## Part 4 - category stats at interval
```bash
scrapy crawl yamlspider \
    -s LOG_LEVEL=INFO \
    -s CLOSESPIDER_ITEMCOUNT=300 \
    -s CATEGORY_STATS_ENABLED=1 \
    -s LOGSTATS_INTERVAL=10 \
    -a config=configs/theurge.yaml \
    -o output/theurge.jl
```

