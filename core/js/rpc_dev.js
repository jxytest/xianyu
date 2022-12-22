rpc.exports = {
    getsign: function (data) {
        console.log("get_sign");
        Java.perform(function () {
           Java.choose("mtopsdk.framework.domain.MtopContext", {
                onMatch: function (instance) {
                    console.log("Found instance: " + instance);
                    var f6253a = instance.b;
                    console.log(f6253a);
                    var api = f6253a.getApiName();
                    console.log(api);
                    send({ "sign": 'api'});
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
    getsign2: function (data) {
        console.log("get_sign");
        Java.perform(function () {
            console.log("get_sign");
            var a = Java.use("com.alibaba.wireless.security.open.middletier.IUnifiedSecurityComponent").$new();
            console.log(a);
            console.log("1");
            var hashMap = Java.use("java.util.HashMap").new();
            hashMap.put("api", "mtop.taobao.idlemtopsearch.search");
            var res = a.getSecurityFactors(hashMap);
            console.log(res);
        });
    }
};
