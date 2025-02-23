package yao.onlinerecord.entity;

//import io.swagger.annotations.ApiModel;
//import io.swagger.annotations.ApiModelProperty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;
import java.sql.Timestamp;

//@ApiModel(value="用户表")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Users implements Serializable {
//    @ApiModelProperty(value = "题目id")
    private int userId;

//    @ApiModelProperty(value = "账号")
    private String account;

//    @ApiModelProperty(value = "用户名")
    private String username;

//    @ApiModelProperty(value = "密码")
    private String password;


    //    @ApiModelProperty(value = "创建时间")
    private Timestamp createdAt;

//    @Override
//    public String toString() {
//        return "Users{" +
//                "userId=" + userId +
//                ", account='" + account + '\'' +
//                ", username='" + username + '\'' +
//                ", password='" + password + '\'' +
//                ", createdAt=" + createdAt +
//                '}';
//    }
}
