# Technical Challenge

## Part 1
```bash
scrapy crawl part1 -s LOG_LEVEL=INFO -s CLOSESPIDER_ITEMCOUNT=300 -o output/products.jl
```

## Part 2
```bash
scrapy crawl part2 -s LOG_LEVEL=INFO -s CLOSESPIDER_ITEMCOUNT=300 -a config=configs/womens-dresses.yaml -o output/womens-dresses.jl
```

