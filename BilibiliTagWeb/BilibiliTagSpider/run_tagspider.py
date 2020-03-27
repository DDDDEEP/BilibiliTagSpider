from scrapy import cmdline

type_id = 17
time_from = 20170101
time_to = 20170101
command = "scrapy crawl tagspider -a type_id={type_id} time_from={time_from} time_to={time_from}".format(
    type_id = type_id,
    time_from = time_from,
    time_to = time_to,
)
cmdline.execute(command.split())