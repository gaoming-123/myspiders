#! /usr/bin/env bash
# /usr/local/service/shell_log/"shell_data.log $(date '+%Y-%m-%d')" 日志文路径
#  for start salve spider
do_start_slave () {
#	echo 'start slave......'
    echo ""
    echo "$(date '+%Y-%m-%d %H:%M:%S') - begin start slave spider......."

    my_ret=$(ps -aux | grep "scrapy crawl bid_tender" | grep -v grep | grep -v "scrapy crawl bid_tender_master" | wc -l)
    if [ x"$1" = x ]; then
        echo "no cmd param!"
        total_process=8
    else
        total_process=$1
    fi
    echo "存活的slave进程数: $my_ret, 需要开启slave的总进程数, $total_process"
    cd /usr/local/service/bid_tender/bid_tender/
    # 循环启动 scrapy project name, 暂定20个进程，后台运行.
#    for((i=0;i<2;i++))
#    do
#        for((j=0;j<10;j++))
#        do
#            nohup scrapy crawl bid_tender > /dev/null 2>&1 &
#        done
#        echo "sleep 30 second"
#        sleep 30
#    done

    for((j=$my_ret;j<$total_process;j++))
    do
        nohup scrapy crawl bid_tender > /dev/null 2>&1 &
        sleep 10
    done

    echo "$(date '+%Y-%m-%d %H:%M:%S') - end start slaves spider......"
}

#  for start master spider
do_start_master () {
#	echo 'start master.....'
    echo ""
    echo "$(date '+%Y-%m-%d %H:%M:%S') - begin start master spider......."
    cd /usr/local/service/bid_tender/bid_tender/
    nohup scrapy crawl bid_tender_master > /dev/null 2>&1 &
    echo "$(date '+%Y-%m-%d %H:%M:%S') - end start master spider......."
}

#  for check master spider
do_check_master () {
    #	echo 'start check master.....'
    echo ""
    echo "$(date '+%Y-%m-%d %H:%M:%S') - begin check master spider......."
    my_ret=`ps aux | grep 'scrapy crawl bid_tender_master' | grep -v grep | wc -l`
    if [ $my_ret -eq 0 ]; then
        do_start_master
    else
        echo "$(date '+%Y-%m-%d %H:%M:%S') - master spider still alive......"
    fi

    echo "$(date '+%Y-%m-%d %H:%M:%S') - end check master spider......."
}

#  for stop all salve spider
do_stop_slave () {
#	echo 'stop salve spiders.....'
    echo ""
    echo "$(date '+%Y-%m-%d %H:%M:%S') - begin stop salve......."
    ps -aux | grep "scrapy crawl bid_tender" | grep -v grep | grep -v "scrapy crawl bid_tender_master" | cut -c 9-15 | xargs kill -9
    echo "$(date '+%Y-%m-%d %H:%M:%S') - end stop salve......."
}

#  for stop master spider
do_stop_master () {
#	echo 'stop master spiders.....'
    echo ""
    echo "$(date '+%Y-%m-%d %H:%M:%S') - begin stop master......."
    ps -aux | grep "scrapy crawl bid_tender_master" | grep -v grep | cut -c 9-15 | xargs kill -9
    echo "$(date '+%Y-%m-%d %H:%M:%S') - end stop master......."
}

# for start download task
do_download_task () {
    echo ""
    echo "$(date '+%Y-%m-%d %H:%M:%S') - begin run download task......"
    _ret=`ps aux | grep '/usr/local/service/bid_tender/bid_tender/config/download.py' | grep -v grep | wc -l`
    if [ $_ret -eq 0 ]; then
        nohup python3 /usr/local/service/bid_tender/bid_tender/config/download.py > /dev/null 2>&1 &
    else
        echo "$(date '+%Y-%m-%d %H:%M:%S') - download_task still alive......"
    fi
    echo "$(date '+%Y-%m-%d %H:%M:%S') - end download task ......"
}

# for clear the url_list data
do_clear_url () {
#	echo 'clear the url_list data......'
    echo ""
    echo "$(date '+%Y-%m-%d %H:%M:%S') - begin run sc_cq_clear_url_list_task......"
    python3 /usr/local/service/bid_tender/bid_tender/task/sc_cq_clear_url_list_task.py
    echo "$(date '+%Y-%m-%d %H:%M:%S') - end sc_cq_clear_url_list_task ......"
}

do_clear_log () {
    echo ""
    echo "$(date '+%Y-%m-%d %H:%M:%S') - begin clear spider log......"
    ip_add=`/sbin/ifconfig eth0 | grep 'inet ' | awk '{print $2}'`
    cd /usr/local/service/spider_log/
    cp mySpider_${ip_add}.log mySpider_`date -d "-10 minutes" +"%Y%m%d%H%M"`_${ip_add}.log
    echo '' > mySpider_${ip_add}.log
    rm mySpider_`date -d "-25 hours" +"%Y%m%d%H"`*.log -f
    echo "$(date '+%Y-%m-%d %H:%M:%S') - end clear spider log......"
}

do_del_log () {
    echo ""
    echo "$(date '+%Y-%m-%d %H:%M:%S') - begin run sc_cq_clear_url_list_task......"
    find /usr/local/service/shell_log -name "shell_data.log*" -type f -mtime +7 -exec rm -f {} \;
    echo "$(date '+%Y-%m-%d %H:%M:%S') - end sc_cq_clear_url_list_task ......"
}

do_add_url () {
    echo ""
    echo "$(date '+%Y-%m-%d %H:%M:%S') - begin run push_tender_link_task......"
    python3 /usr/local/service/bid_tender/bid_tender/task/push_tender_link_task.py $1;
    echo "$(date '+%Y-%m-%d %H:%M:%S') - end push_tender_link_task ......"
}

case "$1" in
    --start_slave)
        do_start_slave $2 >> /usr/local/service/shell_log/"shell_data.log $(date '+%Y-%m-%d')"
        ;;
    --start_master)
	    do_start_master >> /usr/local/service/shell_log/"shell_data.log $(date '+%Y-%m-%d')"
        ;;
    --check_master)
        do_check_master >> /usr/local/service/shell_log/"shell_data.log $(date '+%Y-%m-%d')"
        ;;
    --stop_slave)
        do_stop_slave >> /usr/local/service/shell_log/"shell_data.log $(date '+%Y-%m-%d')"
        ;;
    --stop_master)
        do_stop_master >> /usr/local/service/shell_log/"shell_data.log $(date '+%Y-%m-%d')"
        ;;
    --stop_all)
        #  for stop all spider, contains slave and master
        echo "---------------------------------start stop all -------------------------------" >> /usr/local/service/shell_log/"shell_data.log $(date '+%Y-%m-%d')"
        do_stop_master >> /usr/local/service/shell_log/"shell_data.log $(date '+%Y-%m-%d')"
	    sleep 5
        do_stop_slave >> /usr/local/service/shell_log/"shell_data.log $(date '+%Y-%m-%d')"
        echo "---------------------------------end stop all-------------------------------" >> /usr/local/service/shell_log/"shell_data.log $(date '+%Y-%m-%d')"
        ;;
    --restart_slave)
	    #  for restart slave spider
	    echo "---------------------------------start restart slave------------------------------" >> /usr/local/service/shell_log/"shell_data.log $(date '+%Y-%m-%d')"
        do_stop_slave >> /usr/local/service/shell_log/"shell_data.log $(date '+%Y-%m-%d')"
        sleep 5
        do_start_slave $2 >> /usr/local/service/shell_log/"shell_data.log $(date '+%Y-%m-%d')"
        echo "---------------------------------end restart slave------------------------------" >> /usr/local/service/shell_log/"shell_data.log $(date '+%Y-%m-%d')"
        ;;
    --restart_master)
	    #  for restart master spider
	    echo "---------------------------------start restart master------------------------------" >> /usr/local/service/shell_log/"shell_data.log $(date '+%Y-%m-%d')"
        do_stop_master >> /usr/local/service/shell_log/"shell_data.log $(date '+%Y-%m-%d')"
        sleep 5
        do_start_master >> /usr/local/service/shell_log/"shell_data.log $(date '+%Y-%m-%d')"
        echo "---------------------------------end restart master------------------------------" >> /usr/local/service/shell_log/"shell_data.log $(date '+%Y-%m-%d')"
        ;;
    --restart_all)
	    #  for restart all spider, contains slave and master
	    echo "---------------------------------end start restart all--------------------------------" >> /usr/local/service/shell_log/"shell_data.log $(date '+%Y-%m-%d')"
        do_stop_master >> /usr/local/service/shell_log/"shell_data.log $(date '+%Y-%m-%d')"
        sleep 1
        do_stop_slave >> /usr/local/service/shell_log/"shell_data.log $(date '+%Y-%m-%d')"
        sleep 5
        do_start_slave >> /usr/local/service/shell_log/"shell_data.log $(date '+%Y-%m-%d')"
        sleep 1
        do_start_master >> /usr/local/service/shell_log/"shell_data.log $(date '+%Y-%m-%d')"
        echo "---------------------------------end restart all--------------------------------" >> /usr/local/service/shell_log/"shell_data.log $(date '+%Y-%m-%d')"
        ;;
    --clear_url)
        do_clear_url >> /usr/local/service/shell_log/"shell_data.log $(date '+%Y-%m-%d')"
        ;;
    --clear_log)
        do_clear_log >> /usr/local/service/shell_log/"shell_data.log $(date '+%Y-%m-%d')"
        ;;
    --del_log)
        do_del_log >> /usr/local/service/shell_log/"shell_data.log $(date '+%Y-%m-%d')"
        ;;
    --add_url)
        do_add_url $2 >> /usr/local/service/shell_log/"shell_data.log $(date '+%Y-%m-%d')"
        ;;
    --download_task)
        do_download_task $2 >> /usr/local/service/shell_log/"shell_data.log $(date '+%Y-%m-%d')"
        ;;
    --help|-h)
        echo '
    use the args as flollow:
        --start_slave [num]:        开启num个进程数的slave爬虫, 不传num系统默认开启8个进程, 由于配置问题, 建议num合理传参;
        --start_master:             开启master爬虫, 只开一个进程;
        --check_master:             检查master爬虫是否存活;
        --stop_slave:               停止所有slave爬虫;
        --stop_master:              停止master爬虫;
        --stop_all:                 停止所有 slave 和 master 爬虫;
        --restart_slave [num]:      重启num个进程数slave爬虫, 会结束之前的所有slave进程;
        --restart_master:           重启master爬虫;
        --restart_all:              重启所有 slave (进程数只能是默认数量) 和 master 爬虫;
        --clear_url:                清理url_lists数据, 默认保留一个月内的所有数据;
        --clear_log:                只清理spider产生的日志;
        --del_log:                  只删除shell脚本产生的且超过7天的日志, 不会清理爬虫产生的日志;
        --download_task:            开启下载附件的任务;
        --add_url [param]:          执行项目的push_tender_link_task.py脚本, 往url_list写数据, param可选参数(不传为all):
                                        # cgw:采购网
                                        # bxw:比选网
                                        # sc_jyw:四川公共资源交易网
                                        # cq_jyw:重庆交易网
                                        # cq_cgw:重庆采购网
                                        # gz_cgw:贵州采购网
                                        # gz_ggzy:贵州公共资源
                                        # yn_cgw:云南采购
                                        # yn_ggzy:云南公共资源
        --help | -h:                查看帮助;
	'
        ;;
    *)
        echo '
    使用 --help | -h 查看可使用参数;
    '
        ;;
esac
