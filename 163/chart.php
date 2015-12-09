<?php 

error_reporting(E_ERROR | E_WARNING | E_PARSE | E_NOTICE);

define('TABLE', 'duobao_all');

class Mysql
{
    public $con = null;

    public function __construct()
    {
        $con = mysql_connect('127.0.0.1', 'root', '');
        if ($con) 
        {
            mysql_query('set names utf8');
            mysql_selectdb('test2');

            return $this->con = $con;
        }
        else
            die('数据库连接失败!');
    }

    public function findOne($sql)
    {
        $rs = mysql_query($sql);
        return mysql_fetch_row($rs);
    }

    public function findAll($sql)
    {
        $res = [];
        $rs = mysql_query($sql);
        while ($row = mysql_fetch_assoc($rs)) 
        {
            $res[] = $row;
        }

        return $res;
    }
}

function findMaxCity($arr, $filter)
{
    $arr = $arr[$filter];
    $arr_len = count($arr);
    $max = 0;
    $max_city = '';

    for ($i = 0; $i < $arr_len; $i++)
    {
        if ($arr[$i][0] > $max)
        {
            $max = $arr[$i][0];
            $max_city = $arr[$i][1];
        }
    }

    return $max_city;
}

// 全国奖品数量分布
function map()
{
    global $db;

    $province = ['北京', '天津', '上海', '重庆', '河北', '河南', '云南', '辽宁', '黑龙江', '湖南', '安徽', '山东', '新疆', '江苏', '浙江', '江西',
            '湖北', '广西', '甘肃', '山西', '内蒙古', '吉林', '福建', '贵州', '广东', '青海', '西藏', '四川', '宁夏', '海南', '台湾', '香港', '澳门'];

    $res = [];

    foreach( $province as $v )
    {
        $sql = "select count(1) as total, '$v' from ". TABLE ." where owner_ip_addr like '$v%'";
        $res['list'][] = $db->findOne($sql);
    }

    $max = findMaxCity($res, 'list');

    $res['max'] = findProvince($max);

    echo json_encode($res);
}

// 根据省id获取信息
function findProvince($province_id)
{
    global $db;
    $res = [];

    if( !empty($province_id) )
    {
        $sql = "select gname, count(gid) as total from ". TABLE ." where owner_ip_addr like '$province_id%' group by gid order by total desc limit 30";

        $res = $db->findAll($sql);
    }

    return $res;
}

// 相应地区的奖品详情
function mapPie()
{
    global $db;

    $selectedProvince = isset($_GET['province']) ? $_GET['province'] : '';

    echo json_encode(findProvince($selectedProvince));
}

// 中奖用户top20
function userRank()
{
    global $db;
    $cid = isset($_GET['cid']) ? $_GET['cid'] : 0;

    $sql = "select count(1) as total, nickname, cid, avatar_prefix from ". TABLE ." group by cid ORDER BY total desc limit 20";
    $res['list'] = $arr = $db->findAll($sql);
    $res['luckyboy'] = getUserAward($arr[0]['cid']);
    $res['userhistory'] = getUserHistory($arr[0]['cid']);

    echo json_encode($res);
}

//获取某个用户的奖项信息
function getUserAward($cid)
{
    $res = [];
    global $db;

    if( $cid )
    {
        $sql = "select count(1) as total, gname from ". TABLE ." where cid = '$cid' group by gid order by total desc limit 20";
        $res = $db->findAll($sql);
    }

    return $res;
}

// 某用户奖品详情
function userAward()
{
    $cid = isset($_GET['cid']) ? $_GET['cid'] : 0;

    echo json_encode(getUserAward($cid));
}

//获取某个用户的中奖历史
function getUserHistory($cid)
{
    $res = [];
    
    if ($cid)
    {
        $sql = "select gname, nickname, owner_cost, duobao_time, luck_code from ". TABLE ." where cid = '$cid' order by duobao_time asc";
        global $db;
        $res = $db->findAll($sql);
    }

    return $res;
}

//用户中奖历史
function userHistory()
{
    $cid = isset($_GET['cid']) ? $_GET['cid'] : '';

    echo json_encode(getUserHistory($cid));
}

$func = isset($_GET['parm']) ? $_GET['parm'] : '';

if ( function_exists($func) ) 
{
    $db = new mySql();
    $func();
}
