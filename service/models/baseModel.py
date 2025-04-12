# -*- coding: utf-8 -*-
"""基础类操作"""
import datetime
from decimal import Decimal
from sqlalchemy import and_, func
from service.model import db


class BaseModel():
    """基础模型"""

    @classmethod
    def update_conditions(cls, conditions, new_values, is_transaction=False):
        """条件更新"""
        filters = cls.make_filters(conditions=conditions)
        try:
            updated_count = cls.query.filter(and_(*filters)).update(new_values)
            if updated_count:
                if not is_transaction:
                    db.session.commit()
                return True
            return False
        except Exception as e:
            print(str(e))
            db.session.rollback()
            return False

    @classmethod
    def update_in(cls, key, value, new_values, conditions=None):
        """in 的操作update"""
        try:
            if conditions:
                updated_count = cls.query.filter_by(
                    **conditions).filter(
                    getattr(cls, key).in_(value)).update(new_values)
            else:
                updated_count = cls.query.filter(
                    getattr(cls, key).in_(value)).update(new_values)
            if updated_count:
                db.session.commit()
                return True
            return False
        except Exception as e:
            print(str(e))
            db.session.rollback()
            return False

    @classmethod
    def add_multy(cls, data):
        """批量添加"""
        try:
            datas = [cls(**item) for item in data]
            db.session.add_all(datas) # 将 list 中的数据添加到数据库中
            db.session.commit()
            return len(data), 'success'
        except Exception as e:
            print(str(e))
            db.session.rollback()
            return False, str(e)

    @classmethod
    def update_by_id(cls, data, data_id):
        """通过ID 更新数据"""
        try:
            condition = {
                "ID": data_id
            }
            updated_count = cls.query.filter_by(**condition).update(data)
            if updated_count:
                db.session.commit()
                return True
            return False
        except Exception as e:
            print(str(e))
            db.session.rollback()
            return False

    @classmethod
    def add_new(cls, data, is_transaction=False):
        """添加新记录"""
        try:
            new_record = cls(**data)
            db.session.add(new_record)
            if not is_transaction:
                db.session.commit()
                return new_record.id

            return new_record
        except Exception as e:
            print("add error", str(e))
            db.session.rollback()
            return False

    @classmethod
    def delete(cls, conditions):
        """删除"""
        try:
            deleted_count = cls.query.filter_by(**conditions).delete()
            if deleted_count:
                db.session.commit()
                return True
            return False
        except Exception as e:
            print(str(e))
            return False

    @classmethod
    def columns(cls):
        """返回表所有字段"""
        return cls.__table__.columns.keys()

    @classmethod
    def switch_for_json(cls, value):
        """为了输出json格式化部分数据"""
        if isinstance(value, datetime.datetime):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(value, datetime.date):
            return value.strftime('%Y-%m-%d')
        elif isinstance(value, Decimal):
            return str(value)
        return value

    @classmethod
    def to_dict(cls, obj, combin=False):
        """转换对象"""
        if not obj:
            return {}
        columns = cls.columns()
        item_dict = {}

        if not combin:
            for column in columns:
                value = getattr(obj, column)
                if isinstance(value, datetime.datetime):
                    item_dict[column] = value.strftime('%Y-%m-%d %H:%M:%S')
                elif isinstance(value, datetime.date):
                    item_dict[column] = value.strftime('%Y-%m-%d')
                elif isinstance(value, Decimal):
                    item_dict[column] = str(value)
                else:
                    item_dict[column] = value
        else:
            for column in columns:
                item_dict[column] = obj.get(column)
        return item_dict

    @classmethod
    def all(cls):
        """获取数据看所有数据"""
        all_data = cls.query.all()
        data_list = []
        for item in all_data:
            data_list.append(cls.to_dict(item))
        return data_list

    @classmethod
    def get_one_by_id(cls, id):
        """通过id 获取数据"""
        obj = cls.query.filter(cls.id == id).first()
        if not obj:
            return False
        return cls.to_dict(obj)

    @classmethod
    def get_where(cls, conditions, return_fields=None, key=None, order_by=None):
        """根据条件 返回数据，自定义返回字段"""
        haive_columns = cls.columns()
        filters = cls.make_filters(conditions=conditions)
        return_fields = [rfield for rfield in return_fields if rfield in haive_columns] \
            if return_fields else None

        obj = cls.query.filter(and_(*filters))
        if order_by:
            for field_name, direction in order_by.items():
                field = getattr(cls, field_name, None)
                if field:
                    if direction.lower() == "asc":
                        obj = obj.order_by(field.asc())
                    elif direction.lower() == "desc":
                        obj = obj.order_by(field.desc())
                    else:
                        continue
                else:
                    continue
        db_result = obj.all()
        # 打印sql
        # print(obj.statement)
        result = [] if not key else {}
        if db_result:
            for item in db_result:
                item_value = cls.to_dict(item)
                if return_fields:
                    item = {field: item_value[field]
                            for field in return_fields}
                else:
                    item = item_value
                if key:
                    result[item_value[key]] = item
                else:
                    result.append(item)

        return result

    @classmethod
    def count_where(cls, conditions=None):
        """统计数量"""
        if conditions:
            # 根据条件构建过滤器
            filters = cls.make_filters(conditions=conditions)
            # 通过过滤条件来计算数量
            count_query = cls.query.filter(and_(*filters))
            result = count_query.with_entities(func.count()).scalar()
        else:
            result = cls.query.with_entities(func.count()).scalar()
        return result if result else 0

    @classmethod
    def all_define_key_value(cls, key="id"):
        """获取所有数据,自定义key"""
        all_data = cls.query.all()
        data_list = {}
        for item in all_data:
            new_item = cls.to_dict(item)
            data_list[new_item[str(key)]] = new_item
        return data_list

    @classmethod
    def all_where_define_key_value(cls, conditions=False, key="id"):
        """根据条件 获取所有数据，并自定义key"""
        if conditions:
            all_data = cls.query.filter_by(**conditions).all()
        else:
            all_data = cls.query.all()

        data_list = {}
        for item in all_data:
            new_item = cls.to_dict(item)
            data_list[new_item[str(key)]] = new_item
        return data_list

    @classmethod
    def get_one_where(cls, conditions, order_by: dict = None):
        """根据条件获取一条"""
        filters = cls.make_filters(conditions=conditions)
        if order_by is None:
            result = cls.query.filter(and_(*filters)).first()
        else:
            obj = cls.query.filter(and_(*filters))
            for field_name, direction in order_by.items():
                field = getattr(cls, field_name, None)
                if field:
                    if direction.lower() == "asc":
                        obj = obj.order_by(field.asc())
                    elif direction.lower() == "desc":
                        obj = obj.order_by(field.desc())

            result = obj.first()

        if not result:
            return False
        return cls.to_dict(result)

    @classmethod
    def get_number_where(cls, conditions, number=None, order_by=None, ):
        """获取前N条"""
        if order_by is None:
            if isinstance(number, int) and number > 0:
                data = cls.query.filter_by(**conditions).limit(number).all()
            else:
                data = cls.query.filter_by(**conditions).all()
        else:
            obj = cls.query.filter_by(**conditions)
            for field_name, direction in order_by.items():
                field = getattr(cls, field_name, None)
                if field:
                    if direction.lower() == "asc":
                        obj = obj.order_by(field.asc())
                    elif direction.lower() == "desc":
                        obj = obj.order_by(field.desc())
                    else:
                        continue
                else:
                    continue
            if isinstance(number, int) and number > 0:
                data = obj.limit(number).all()
            else:
                data = obj.all()
        if not data:
            return []

        result = []
        for item in data:
            result.append(cls.to_dict(item))
        return result

    @classmethod
    def get_show_data(cls, condition, replace_key=None, pop_key=None):
        """获取分页数据"""
        if not condition:
            return []
        conditions = condition.get('where', {})
        limit = condition.get('limit', None)
        order = condition.get('order', None)
        pagesize = int(
            condition.get('pagesize', 10)) if 'pagesize' in condition and str(condition['pagesize']).isdigit() else 10
        page = int(condition['page']) if 'page' in condition and str(condition['page']).isdigit(
        ) else 1
        filters = cls.make_filters(conditions)
        if len(filters) > 0:
            obj = cls.query.filter(and_(*filters))
        else:
            obj = cls.query
        if order and len(order) > 0:
            for field_name, direction in order.items():
                field = getattr(cls, field_name, None)
                if field:
                    if direction.lower() == "asc":
                        obj = obj.order_by(field.asc())
                    elif direction.lower() == "desc":
                        obj = obj.order_by(field.desc())
                    else:
                        direction = getattr(cls, direction)
                        if direction:
                            obj = obj.order_by(field == direction)
                        continue
        count_query = cls.query.filter(
            and_(*filters)).with_entities(func.count())
        all_count = count_query.scalar()
        if not all_count:
            all_count = 0
        if limit is not None:
            data = obj.limit(limit).all()

        else:
            # 分页
            if page is None:
                page = 1
            data = obj.offset((page - 1) * pagesize).limit(pagesize).all()
        # 打印sql
        # print(obj.statement)

        result = []
        for item in data:
            item_dict = cls.to_dict(item)
            # 处理replace
            if replace_key is not None:
                for key, value in replace_key.items():
                    if key in item_dict:
                        item_dict[key] = value[item_dict[key]]
            # 处理pop
            if isinstance(pop_key, list):
                for key in pop_key:
                    if key in item_dict:
                        item_dict.pop(key)

            result.append(item_dict)
        return {
            'data': result,
            'all_count': all_count,
            'page': page,
            'max_page': (all_count+pagesize-1) // pagesize
        }

    @classmethod
    def make_filters(cls, conditions):
        """创建筛选"""
        haive_columns = cls.columns()
        filters = []
        for key, condition in conditions.items():
            if key not in haive_columns:
                continue
            field = getattr(cls, key)
            if isinstance(condition, dict) or isinstance(condition, list):
                if isinstance(condition, dict) and 'operator' in condition and 'value' in condition:
                    op = condition.get('operator')
                    value = condition.get('value')
                elif len(condition) == 2:
                    op = condition[0]
                    value = condition[1]
                else:
                    continue

                if op == '>':
                    filters.append(field > value)
                elif op == '<':
                    filters.append(field < value)
                elif op == '>=':
                    filters.append(field >= value)
                elif op == '<=':
                    filters.append(field <= value)
                elif op in ['<>', '!=']:
                    filters.append(field != value)
                elif op == 'in':
                    if isinstance(value, str):
                        value = [value]
                    filters.append(field.in_(value))
                elif op == 'like':  # 模糊搜索
                    filters.append(field.like('%'+str(value)+'%'))
                elif op == 'ilike':  # 模糊搜索 不区分大小写
                    filters.append(field.ilike('%'+str(value)+'%'))
                else:  # between 两者之间
                    filters.append(field.between(op, value))
            else:
                filters.append(field == str(condition))
        return filters

    @classmethod
    def get_distinct(cls, distinct_field: list = [], conditions: dict = None):
        """取去除重复后的值"""
        if len(distinct_field) == 0:
            return []
        # 获取所有字段
        all_columns = cls.columns()
        # 获取需要查询的字段
        use_field = []
        query_fields = []
        for field in distinct_field:
            if field not in all_columns:
                continue
            query_fields.append(getattr(cls, field))
            use_field.append(field)
        if len(query_fields) == 0:
            return []

        obj = cls.query.with_entities(*query_fields)
        filters = cls.make_filters(conditions)
        data = obj.filter(*filters).distinct().all()
        result = [{use_field[i]: row[i]
                   for i in range(len(use_field))} for row in data]

        return result

    @classmethod
    def get_sum(cls, fields: list = [], conditions: dict = None):
        """求和某个字段"""
        if len(fields) == 0:
            return {}
        # 获取所有字段
        all_columns = cls.columns()
        # 获取需要查询的字段
        query_fields = []
        use_fields = []
        for field in fields:
            if field not in all_columns:
                continue
            query_fields.append(getattr(cls, field))
            use_fields.append(field)
        if len(query_fields) == 0:
            return {}
        obj = cls.query.with_entities(func.sum(*query_fields))
        filters = cls.make_filters(conditions)
        data = obj.filter(*filters).all()
        result = {use_fields[i]: data[0]
                  for i in range(len(use_fields))}

        return result
