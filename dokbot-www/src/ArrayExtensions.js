window.Array.prototype.orderBy = function (valueSelector) {
  var result = this.slice(0).sort(function (a, b) {
    var leftValue = valueSelector ? valueSelector(a) : a;
    var rightValue = valueSelector ? valueSelector(b) : b;
    return (leftValue < rightValue) ? -1 : (leftValue === rightValue ? 0 : 1);
  });
  return result;
};
window.Array.prototype.groupBy = function (keySelector, valueSelector) {
  var result: any = {};
  for (var i = 0; i < this.length; ++i) {
    var item = this[i];
    var key = keySelector(item);
    if (!(key in result)) result[key] = [];
    var value = valueSelector ? valueSelector(item) : item;
    result[key].push(value);
  }
  return result;
};
window.Array.prototype.except = function (items, comparator) {
  const result = [];
  comparator = comparator || ((l, r) => l === r);
  for (let i = 0; i < this.length; i++) {
    let item = this[i];
    let found = false;
    for (let j = 0; j < items.length; j++) {
      if (comparator(item, items[j])) {
        found = true;
      }
    }
    if (!found) {
      result.push(item);
    }
  }
  return result;
};