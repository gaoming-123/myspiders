from bid_tender.piplines import *
from bid_tender.provinces import *

class CommPipeline(object):
    def process_item(self, item, spider):
        pipe_name=''
        if ('pipline_func' in item):
            spider.logger.info("commpipline start, item type is: " + item['pipline_func'])
            eval(item['pipline_func'] + '(item)')
            pipe_name=item['pipline_func']
        elif ('pipeline_func' in item):
            spider.logger.info("commpipeline start, item type is: " + item['pipeline_func'])
            eval(item['pipeline_func'] + '(item)')
            pipe_name = item['pipeline_func']
        else:
            spider.logger.warning("commpipline start, but no item cfg")
        spider.logger.info("commpipline end, item type is: " + pipe_name )
        return item