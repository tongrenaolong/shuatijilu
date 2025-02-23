package yao.onlinerecord;

import lombok.extern.slf4j.Slf4j;
import org.mybatis.spring.annotation.MapperScan;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@Slf4j
@SpringBootApplication
@MapperScan("yao.onlinerecord.mapper")
public class OnlineRecordApplication {
//	private static final Logger log = LoggerFactory.getLogger(OnlineRecordApplication.class);

	public static void main(String[] args) {
		log.info("项目启动");
		SpringApplication.run(OnlineRecordApplication.class, args);
	}

}
