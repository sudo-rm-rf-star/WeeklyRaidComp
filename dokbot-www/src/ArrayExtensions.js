window.Array.prototype.orderBy = function (valueSelector) {
  return this.slice(0).sort((a, b) => {
    const leftValue = valueSelector ? valueSelector(a) : a;
    const rightValue = valueSelector ? valueSelector(b) : b;
    return (leftValue < rightValue) ? -1 : (leftValue === rightValue ? 0 : 1);
  });
};
window.Array.prototype.groupBy = function (keySelector, valueSelector) {
  const result = {};
  for (let i = 0; i < this.length; ++i) {
    const item = this[i];
    const key = keySelector(item);
    if (!(key in result)) result[key] = [];
    const value = valueSelector ? valueSelector(item) : item;
    result[key].push(value);
  }
  return result;
};

window.Array.prototype.groupByRole = function () {
  return this.groupBy((x) => x.role);
};

window.Array.prototype.except = function (items, comparator) {
  const result = [];
  comparator = comparator || ((l, r) => l === r);
  for (let i = 0; i < this.length; i++) {
    const item = this[i];
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

window.Array.prototype.max = function (valueSelector) {
  let max = 0;
  this.forEach((x) => {
    const value = valueSelector ? valueSelector(x) : x;
    max = value > max ? value : max;
  });
  return max;
};

window.Array.prototype.uniqueBy = function( valueSelector ) {
  return [...new Map(this.map(item => [valueSelector(item), item])).values()];
}

window.Array.prototype.uniqueById = function () {
  return this.uniqueBy(({id}) => id)
}