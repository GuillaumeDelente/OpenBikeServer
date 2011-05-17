/*
 * Copyright (C) 2011 Guillaume Delente
 *
 * This file is part of OpenBikeServer.
 *
 * OpenBikeServer is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, version 3 of the License.
 *
 * OpenBikeServer is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with OpenBikeServer.  If not, see <http://www.gnu.org/licenses/>.
 */
package fr.openbike;

/**
 * @author guitou
 * 
 */
public class Utils {

	public static final String romansRegexp[] = { "Ii ", "Iii ", "Iv ", "Vi ",
			"Vii ", "Viii ", "Ix ", "Xi ", "Xii ", "Xiii ", "Xiv ", "Xv ",
			"Xvi ", "Xvii ", "Xviii ", "Xix ", "Xx ", "Xxi ", "Xxii ",
			"Xxiii ", "Xxiv ", "Xxv " };

	public static final String romans[] = { "II ", "III ", "IV ", "VI ",
			"VII ", "VIII ", "IX ", "XI ", "XII ", "XIII ", "XIV ", "XV ",
			"XVI ", "XVII ", "XVIII ", "XIX ", "XX ", "XXI ", "XXII ",
			"XXIII ", "XXIV ", "XXV " };

	public static String capitalizeFully(String str) {
		String result = capitalizeFully(str, null);
		result += " ";
		for (int i = 0; i < romans.length; i++) {
			result = result.replace(romansRegexp[i], romans[i]);
		}
		result = result.trim();
		return result;
	}

	public static String capitalizeFully(String str, char[] delimiters) {
		int delimLen = (delimiters == null ? -1 : delimiters.length);
		if (str == null || str.length() == 0 || delimLen == 0) {
			return str;
		}
		str = str.toLowerCase();
		return capitalize(str, delimiters);
	}

	public static String capitalize(String str) {
		return capitalize(str, null);
	}

	public static String capitalize(String str, char[] delimiters) {
		int delimLen = (delimiters == null ? -1 : delimiters.length);
		if (str == null || str.length() == 0 || delimLen == 0) {
			return str;
		}
		int strLen = str.length();
		StringBuffer buffer = new StringBuffer(strLen);
		boolean capitalizeNext = true;
		for (int i = 0; i < strLen; i++) {
			char ch = str.charAt(i);

			if (isDelimiter(ch, delimiters)) {
				buffer.append(ch);
				capitalizeNext = true;
			} else if (capitalizeNext) {
				buffer.append(Character.toTitleCase(ch));
				capitalizeNext = false;
			} else {
				buffer.append(ch);
			}
		}
		return buffer.toString();
	}

	private static boolean isDelimiter(char ch, char[] delimiters) {
		if (delimiters == null) {
			return Character.isWhitespace(ch);
		}
		for (int i = 0, isize = delimiters.length; i < isize; i++) {
			if (ch == delimiters[i]) {
				return true;
			}
		}
		return false;
	}
}
