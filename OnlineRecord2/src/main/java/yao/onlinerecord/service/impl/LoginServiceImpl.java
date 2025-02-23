package yao.onlinerecord.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import yao.onlinerecord.entity.Users;
import yao.onlinerecord.mapper.UsersMapper;
import yao.onlinerecord.service.LoginService;

import java.util.List;

@Service
public class LoginServiceImpl implements LoginService {

    @Autowired
    private UsersMapper usersMapper;
    @Override
    public List<Users> list() {
        return usersMapper.GetUserList();
    }
}
