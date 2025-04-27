package com.parallelism.fake.init;

import com.parallelism.fake.entity.User;
import com.parallelism.fake.repository.UserRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class DataInitializer {

    @Bean
    CommandLineRunner initDatabase(UserRepository repository) {
        return args -> {
            repository.save(new User(null, "alice@example.com", "Alice"));
            repository.save(new User(null, "bob@example.com", "Bob"));

            System.out.println("Sample users have been initialized in the database");
        };
    }
}
