
function convertToPercentage(pace) {
    if(pace=== '')
        {return}
    var percentageValue = pace
    var displayValue = (percentageValue * 100).toFixed(1) + '%'; // 转换为百分比形式，并保留两位小数

    return displayValue;
}
//计算离月底还剩余多少天？
function getRemainingDaysInMonth(in_date) {
// 获取当前日期
    // var today = new Date();
    // console("in_date:"+in_date);
    // alert(in_date);
    var date = new Date(in_date)
    // 获取本月的最后一天
    var lastDay = new Date(date.getFullYear(), date.getMonth() + 1, 0);
    // 计算剩余天数
    var remainingDays = lastDay.getDate() - date.getDate();
    return remainingDays;
}

// 导出函数，如果你使用模块系统
// export { convertToPercentage, getRemainingDaysInMonth };