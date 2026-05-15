package com.ai.controller;

import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
public class DetectionController {

    @GetMapping("/test")
    public String test() {
        return "Backend Running";
    }
}
