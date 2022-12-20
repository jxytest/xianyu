// 定义需要重复使用的字符串
const DATA = 'data';
const DEVICE_ID = 'deviceId';
const SID = 'sid';
const X_FEATURES = 'x-features';
const APP_KEY = 'appKey';
const API = 'api';
const LAT = 'lat';
const LNG = 'lng';
const UTDID = 'utdid';
const EXTDATA = 'extdata';
const TTID = 'ttid';
const T = 't';
const V = 'v';
const PAGE_ID = 'pageId';
const PAGE_NAME = 'pageName';
// 定义 HashMap 对象和 String 对象
const hashMap = Java.use('java.util.HashMap');
const string = Java.use('java.lang.String');

function hashPut(hashMap, key, value) {
    hashMap.put(string.$new(key), string.$new(value));
}

// 创建 h1 和 h2 两个 HashMap 对象
let h1 = hashMap.$new();
let h2 = hashMap.$new();
hashPut(h1, DEVICE_ID, "AlvatDNiQ9bO-NjCHnL-ZNlIKZbclZyNDd49TQakZCXT");
hashPut(h1, SID, "15c5a4a80dd415edaad88cea2afe78c0");
hashPut(h1, X_FEATURES, "27");
hashPut(h1, APP_KEY, "21407387");
hashPut(h1, API, "mtop.taobao.idlemtopsearch.search");
hashPut(h1, LAT, "0");
hashPut(h1, LNG, "0");
hashPut(h1, UTDID, "Y5wu32PRazMDAKz6FvVOHBHu");
hashPut(h1, EXTDATA, 'openappkey=DEFAULT_AUTH')
hashPut(h1, TTID, "231200@fleamarket_android_7.8.40");
hashPut(h1, V, "1.0");
hashPut(h1, PAGE_ID, "");
hashPut(h1, PAGE_NAME, "");
let s1 = string.$new("21407387");
let s2 = string.$new();
let s3 = string.$new('r_117');


rpc.exports = {
    getsign: function(data, t) {
        Java.perform(function() {
            console.log("get_sign");
            console.log(s3);
            // 每次调用，更新data
            hashPut(h1, DATA, data);
            // var t = Math.floor(new Date().getTime() / 1000).toString();
            // 每次调用 getsign 函数时，都会更新 t 的值
            hashPut(h1, T, t);
            Java.choose("mtopsdk.security.InnerSignImpl", {
                onMatch: function (instance) {
                    console.log("Found instance: " + instance);
                    var result = instance.getUnifiedSign(h1, h2, s1, s2, true, s3);
                    console.log(result);
                    send({ "sign": result.toString()});
                    // 必须返回stop，否则会遍历所有的实例
                    return "stop";
                },
                onComplete: function () {
                    console.log("Done");
                },
                // 使用 onMatchOnce: true 选项
                onMatchOnce: true
            });
        });
    },
};
// hook mtopsdk.mtop.global.SwitchConfig，返回false，禁用spdy协议，可以进行抓包
Java.perform(function() {
    var SwitchConfig = Java.use('mtopsdk.mtop.global.SwitchConfig');
    SwitchConfig.A.overload().implementation = function () {
        return false;
    }
});
