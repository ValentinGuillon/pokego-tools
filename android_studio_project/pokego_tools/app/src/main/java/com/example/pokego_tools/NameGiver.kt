package com.example.pokego_tools

import android.content.Intent
import android.os.Bundle
import android.text.Editable
import android.widget.Button
import android.widget.CheckBox
import android.widget.EditText
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity


class NameGiver : AppCompatActivity() {
    private lateinit var statsLayout: EditText
    private lateinit var ivsLayout: EditText
    private lateinit var shadowLayout: CheckBox
    private lateinit var nameLayout: EditText

    private var shadow: Boolean = false

    private lateinit var symbols: List<String>


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.name_giver)
//        enableEdgeToEdge()
//        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
//            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
//            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
//            insets
//        }

        statsLayout = findViewById(R.id.editText_stats)
        ivsLayout = findViewById(R.id.editText_ivs)
        shadowLayout = findViewById(R.id.checkbox_shadow)
        nameLayout = findViewById(R.id.editText_validate)
        symbols = listOf("⓪", "①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧", "⑨", "⑩", "⑪", "⑫", "⑬", "⑭", "⓯")

        listenCheckShadow()
        listenValidation()
        listenClearAll()
        listenClose()
        listenFocuses()
    }

    private fun listenClose() {
        val btnClose = findViewById<Button>(R.id.btn_close)
        btnClose.setOnClickListener {
            val home = Intent(this, MainMenu::class.java)
            startActivity(home)
        }
    }


    private fun listenCheckShadow() {
        shadowLayout.setOnCheckedChangeListener { _, isChecked ->
            shadow = isChecked
        }
    }


    private fun listenClearAll() {
        val btnClear = findViewById<Button>(R.id.btn_clear_all)
        btnClear.setOnClickListener {
            statsLayout.setText("")
            ivsLayout.setText("")
            nameLayout.setText("")
            shadowLayout.isChecked = false
            shadow = false
        }
    }

    private fun listenFocuses() {
        statsLayout.setOnFocusChangeListener { _, hasFocus ->
            if (hasFocus) { statsLayout.setText("") }

        }
        ivsLayout.setOnFocusChangeListener { _, hasFocus ->
            if (hasFocus) { ivsLayout.setText("") }

        }
    }

    private fun listenValidation() {
        val buttonValidate = findViewById<Button>(R.id.button_validate)

        buttonValidate.setOnClickListener {
            updateName()
        }
    }


    private fun updateName() {
        val statsStr = statsLayout.text.toString()
        val ivsStr = ivsLayout.text.toString()

        val stats = strListToIntList(statsStr.split(" "))
        val ivs = strListToIntList(ivsStr.split(" "))

        if (stats.isEmpty() or ivs.isEmpty()) {
            Toast.makeText(this, "Must give 3 numbers separated by space", Toast.LENGTH_SHORT).show()
            return
        }

        val overall = mergeLists(stats, ivs, shadow)

        val averageDefHP: Double = (overall[1] + overall[2]) / 2

        val ivsSymbols: List<String>
        try {
            ivsSymbols = intToSymbol(ivs)
        } catch (_:Exception) {
            Toast.makeText(this, "IVs are between 0 and 15", Toast.LENGTH_SHORT).show()
            return
        }

        val ivsFormate = ivsSymbols.fold("") {acc, element -> acc + element.toString()}
//        val text = "[${statsStr}] + [${ivsStr}] + [${shadow}]"
        val text = "${overall[0].toInt()}${ivsFormate}${averageDefHP.toInt()}"

//        nameLayout.text = "[${stats}] [${ivs}] [${shadow}]"
        nameLayout.text = Editable.Factory.getInstance().newEditable(text)
    }


    private fun mergeLists (l1: List<Int>, l2: List<Int>, shadow: Boolean) : List<Double> {
        val res: MutableList<Double> = mutableListOf()
        for (i in 0 until 3) {
            res.add((l1[i] + l2[i]).toDouble())
        }

        if (shadow) {
            res[0] = res[0] * 1.2
            res[1] = res[1] * 0.8333333
        }

        return res
    }


    private fun strListToIntList (l: List<String>) : List<Int> {
        val res: MutableList<Int> = mutableListOf()
        val i = l.listIterator()

        try {
            i.forEach { v -> res.add(v.toInt())}
        } catch (_: NumberFormatException) {
            res.clear()
        }

        // Return empty list if there is not enough numbers (=3)
        if (res.count() != 3) { res.clear() }
        return res
    }

    private fun intToSymbol (numbers: List<Int>): List<String> {
        return numbers.map { symbols[it] }
    }
}