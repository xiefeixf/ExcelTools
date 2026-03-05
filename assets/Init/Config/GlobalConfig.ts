// 自动生成，请勿手动修改
import {
} from "./ConfigType";
import {
} from "./ConfigData";

export const GlobalConfig: {
} = {
};

/**
 * 根据表名和id获取属性对象
 * @param table 表名（如 'XXX'）
 * @param id 主键id
 */
export function getConfigById(table: keyof typeof GlobalConfig, id: number | string) {
  const arr = GlobalConfig[table];
  if (!Array.isArray(arr)) return undefined;
  return arr.find(item => item.id === id);
}
