package yao.onlinerecord.service;

import yao.onlinerecord.entity.Users;

import java.util.List;

public interface LoginService {
    /**
     * 查询所有用户
     * @return
     */
    List<Users> list();
}
