package yao.onlinerecord.mapper;

import org.apache.ibatis.annotations.Mapper;
import yao.onlinerecord.entity.Users;

import java.util.List;

@Mapper
public interface UsersMapper {
    public List<Users> GetUserList();
}
